from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from loguru import logger
from config import config_manager, LLMModel
from src.services.kubernetes_secret_service import KubernetesSecretService
from src.services.approval_service import ApprovalService
from src.services.email_service import EmailService
from src.litellm.manager import KeyManagement
from src.background.queue_processor import QueueProcessor
from src.models.key_request import KeyRequestState

# Initialize services
k8s_service = KubernetesSecretService(namespace=config_manager.get_kubernetes_namespace())
approval_service = ApprovalService()
email_service = EmailService(config=config_manager.get_smtp_config())
key_manager = KeyManagement()

# Initialize queue processor
queue_processor = QueueProcessor(
    k8s_service=k8s_service,
    approval_service=approval_service,
    email_service=email_service,
    key_manager=key_manager
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for application startup and shutdown.
    
    This replaces the deprecated @app.on_event("startup") and @app.on_event("shutdown")
    decorators with the modern lifespan approach.
    """
    # Startup logic
    logger.info("Starting application...")
    queue_processor.start()
    logger.info("Application started successfully")
    
    yield  # Application runs here
    
    # Shutdown logic
    logger.info("Shutting down application...")
    await queue_processor.stop()
    logger.info("Application shutdown complete")


app = FastAPI(title="LLM Key Requestor API", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
)


class KeyRequest(BaseModel):
    llm: str
    email: str


class KeyResponse(BaseModel):
    message: str
    success: bool
    request_id: Optional[str] = None


class ModelsResponse(BaseModel):
    models: list[LLMModel]


@app.get("/")
async def root():
    return {"message": "LLM Key Requestor API", "status": "active"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/api/models", response_model=ModelsResponse)
def get_models():
    """
    Return list of available LLM models with metadata from configuration.
    Includes both local models and models from LiteLLM if enabled.
    """
    models = config_manager.get_all_models()
    return ModelsResponse(models=models)


@app.post("/api/request-key", response_model=KeyResponse)
async def request_key(request: KeyRequest):
    """
    Handle key request submission.
    
    Process:
    1. Check if a key request already exists for this user's email
    2. If exists, return current approval state
    3. If not exists, create new pending request
    4. Return appropriate response based on outcome
    """
    logger.info(f"Received key request for {request.llm} from {request.email}")
    
    try:
        # Check if request already exists for this email
        existing_request = await k8s_service.find_by_email(request.email)
        
        if existing_request and existing_request.model == request.llm:
            # Request already exists, return current state
            logger.info(f"Found existing request for {request.email} with state {existing_request.state.value} and llm {existing_request.model}")
            
            if existing_request.state == KeyRequestState.PENDING:
                message = f"Your key request for {request.llm} is pending approval. You will be notified via email once approved."
            elif existing_request.state == KeyRequestState.APPROVED:
                message = f"Your key request for {request.llm} has been approved. Check your email for the API key."
            elif existing_request.state == KeyRequestState.DENIED:
                message = f"Your key request for {request.llm} was denied. Please contact support for more information."
            else:
                message = f"Your key request for {request.llm} is being processed."
            
            return KeyResponse(
                message=message,
                success=True,
                request_id=existing_request.request_id
            )
        
        # No existing request, create new one
        new_request = await k8s_service.create(email=request.email, model=request.llm)
        logger.info(f"Created new key request for {request.email}, request_id: {new_request.request_id}")
        
        return KeyResponse(
            message=f"Key request for {request.llm} has been created successfully. You will be notified via email once your request is processed.",
            success=True,
            request_id=new_request.request_id
        )
        
    except Exception as e:
        logger.error(f"Error processing key request for {request.email}: {e}", exc_info=True)
        return KeyResponse(
            message="An error occurred while processing your request. Please try again later.",
            success=False,
            request_id=None
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
