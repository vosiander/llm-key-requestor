from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging
import inspect
from loguru import logger
from config import config_manager, LLMModel
from src.services.kubernetes_secret_service import KubernetesSecretService
from src.services.approval_service import ApprovalService
from src.services.email_service import EmailService
from src.litellm.manager import KeyManagement
from src.background.queue_processor import QueueProcessor
from src.models.key_request import KeyRequestState
from src.mcp import create_mcp_server


# Intercept standard logging and redirect to loguru
class InterceptHandler(logging.Handler):
    """
    Handler to intercept standard logging and redirect to loguru.
    This ensures all logs from libraries using standard logging (like FastMCP, uvicorn)
    are formatted consistently with loguru.
    """
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


# Configure logging to intercept standard library logging
logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

# Intercept specific loggers that might be used by dependencies
for logger_name in ["uvicorn", "uvicorn.access", "uvicorn.error", "fastapi", "mcp"]:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler()]
    logging_logger.propagate = False

# Initialize services
k8s_service = KubernetesSecretService(namespace=config_manager.get_kubernetes_namespace())
approval_service = ApprovalService(plugins=config_manager.get_approval_plugins())
email_service = EmailService(config=config_manager.get_smtp_config())
key_manager = KeyManagement()

# Initialize queue processor
queue_processor = QueueProcessor(
    k8s_service=k8s_service,
    approval_service=approval_service,
    email_service=email_service,
    key_manager=key_manager
)

# Configure MCP server (before FastAPI app creation)
logger.info("Creating MCP server, will mount at /mcp")

# Create MCP server
mcp_server = create_mcp_server(k8s_service=k8s_service,)

# Initialize the streamable HTTP app to create the session manager
mcp_app = mcp_server.streamable_http_app()
logger.info("MCP server created successfully")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for application startup and shutdown.
    
    This replaces the deprecated @app.on_event("startup") and @app.on_event("shutdown")
    decorators with the modern lifespan approach.
    
    Integrates the MCP session manager's lifespan if enabled.
    """
    # Startup logic
    logger.info("Starting application...")
    queue_processor.start()
    
    # Run within MCP session manager context
    logger.info("Starting MCP session manager...")
    async with mcp_server.session_manager.run():
        logger.info("Application started successfully")
        yield  # Application runs here
        logger.info("Shutting down application...")
    
    # Shutdown logic
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

# Mount MCP server at /mcp
logger.info("Mounting MCP server at /mcp")
app.mount("/mcp", mcp_app)
logger.info("MCP server mounted successfully")


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
