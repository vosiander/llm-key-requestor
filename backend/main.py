from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from pydantic import BaseModel
from typing import Optional, List
import logging
import inspect
import secrets
from loguru import logger
from config import config_manager, LLMModel, FeaturedModel
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

# Initialize services using dependency injection
k8s_service = config_manager.injector.get(KubernetesSecretService)
approval_service = config_manager.injector.get(ApprovalService)
email_service = config_manager.injector.get(EmailService)
key_manager = config_manager.injector.get(KeyManagement)
queue_processor = config_manager.injector.get(QueueProcessor)

# Configure MCP server (before FastAPI app creation)
logger.info("Creating MCP server, will mount at /mcp")

# Create MCP server
mcp_server = create_mcp_server(k8s_service=k8s_service,)

# Initialize the streamable HTTP app to create the session manager
mcp_app = mcp_server.http_app()
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
    
    # Start the MCP app's lifespan context
    async with mcp_app.lifespan(mcp_app):
        queue_processor.start()
        logger.info("Application started successfully")
        
        yield  # Application runs here
        
        logger.info("Shutting down application...")
        # Shutdown logic
        await queue_processor.stop()
        logger.info("Application shutdown complete")


app = FastAPI(
    title="LLM Key Requestor API",
    lifespan=lifespan,
    redirect_slashes=False)

# Add ProxyHeadersMiddleware to handle reverse proxy headers (X-Forwarded-Proto, etc.)
# This ensures redirects preserve HTTPS when behind a reverse proxy
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config_manager.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


class FeaturedModelsResponse(BaseModel):
    models: list[FeaturedModel]


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


@app.get("/api/featured-models", response_model=FeaturedModelsResponse)
def get_featured_models():
    """
    Return list of featured/easy-mode models from configuration.
    These are user-friendly models with additional metadata like subtitle and documentation links.
    """
    models = config_manager.get_featured_models()
    return FeaturedModelsResponse(models=models)


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


# Admin Panel Authentication
security = HTTPBasic()


def verify_admin_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Verify admin credentials using HTTP Basic Auth.
    
    Credentials are checked against values from configuration
    (which can be overridden by environment variables).
    """
    admin_config = config_manager.get_admin_config()
    
    is_correct_username = secrets.compare_digest(
        credentials.username.encode("utf8"),
        admin_config.username.encode("utf8")
    )
    is_correct_password = secrets.compare_digest(
        credentials.password.encode("utf8"),
        admin_config.password.encode("utf8")
    )
    
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credentials.username


class KeyRequestResponse(BaseModel):
    request_id: str
    email: str
    model: str
    state: str
    created_at: str
    updated_at: str
    api_key: Optional[str] = None


class DenyRequest(BaseModel):
    reason: str


class AdminActionResponse(BaseModel):
    success: bool
    message: str


@app.post("/api/admin/verify")
async def admin_verify(username: str = Depends(verify_admin_credentials)):
    """Verify admin credentials."""
    return {"authenticated": True, "username": username}


@app.get("/api/admin/requests", response_model=List[KeyRequestResponse])
async def get_admin_requests(
    filter: str = "pending",
    username: str = Depends(verify_admin_credentials)
):
    """
    Get key requests based on filter.
    
    Filter options:
    - pending: Only pending requests
    - review: Only in-review requests
    - all: All requests
    """
    try:
        all_requests = await k8s_service.list_all()
        
        if filter == "pending":
            filtered = [r for r in all_requests if r.state == KeyRequestState.PENDING]
        elif filter == "review":
            filtered = [r for r in all_requests if r.state == KeyRequestState.REVIEW]
        else:
            filtered = all_requests
        
        return [
            KeyRequestResponse(
                request_id=r.request_id,
                email=r.email,
                model=r.model,
                state=r.state.value,
                created_at=r.created_at.isoformat(),
                updated_at=r.updated_at.isoformat(),
                api_key=r.api_key if r.state == KeyRequestState.APPROVED else None
            )
            for r in filtered
        ]
    except Exception as e:
        logger.error(f"Error fetching admin requests: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch requests")


@app.get("/api/admin/requests/{request_id}", response_model=KeyRequestResponse)
async def get_admin_request_details(
    request_id: str,
    username: str = Depends(verify_admin_credentials)
):
    """Get details for a specific request."""
    try:
        request = await k8s_service.get(request_id)
        
        if not request:
            raise HTTPException(status_code=404, detail="Request not found")
        
        return KeyRequestResponse(
            request_id=request.request_id,
            email=request.email,
            model=request.model,
            state=request.state.value,
            created_at=request.created_at.isoformat(),
            updated_at=request.updated_at.isoformat(),
            api_key=request.api_key if request.state == KeyRequestState.APPROVED else None
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching request details: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch request details")


@app.post("/api/admin/requests/{request_id}/approve", response_model=AdminActionResponse)
async def approve_request(
    request_id: str,
    username: str = Depends(verify_admin_credentials)
):
    """Approve a key request."""
    try:
        logger.info(f"Admin {username} approving request {request_id}")
        
        # Get the request
        request = await k8s_service.get(request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Request not found")
        
        # Update state to approved and process
        await k8s_service.update_state(request_id, KeyRequestState.APPROVED)
        
        # Process the approval (generate key, send email, etc.)
        await approval_service.process_approval(request_id)
        
        logger.info(f"Request {request_id} approved by admin {username}")
        
        return AdminActionResponse(
            success=True,
            message=f"Request {request_id} approved successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error approving request {request_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to approve request")


@app.post("/api/admin/requests/{request_id}/deny", response_model=AdminActionResponse)
async def deny_request(
    request_id: str,
    deny_data: DenyRequest,
    username: str = Depends(verify_admin_credentials)
):
    """Deny a key request with reason."""
    try:
        logger.info(f"Admin {username} denying request {request_id} with reason: {deny_data.reason}")
        
        # Get the request
        request = await k8s_service.get(request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Request not found")
        
        # Update state to denied
        await k8s_service.update_state(request_id, KeyRequestState.DENIED)
        
        # Send denial email
        try:
            await email_service.send_denial_email(
                request.email,
                request.model,
                deny_data.reason
            )
        except Exception as email_error:
            logger.error(f"Failed to send denial email: {email_error}")
        
        logger.info(f"Request {request_id} denied by admin {username}")
        
        return AdminActionResponse(
            success=True,
            message=f"Request {request_id} denied successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error denying request {request_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to deny request")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
