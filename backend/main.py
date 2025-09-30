from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
import logging

from config import config_manager, LLMModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="LLM Key Requestor API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
)


class KeyRequest(BaseModel):
    llm: str
    email: EmailStr


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
    In a real implementation, this would:
    1. Validate the request
    2. Generate a unique request ID
    3. Store the request in a database
    4. Send an email with the access key or confirmation
    """
    logger.info(f"Received key request for {request.llm} from {request.email}")
    
    # TODO: Implement actual key generation and email sending logic
    # For now, just return a success response
    
    return KeyResponse(
        message=f"Key request for {request.llm} received. Check your email at {request.email}",
        success=True,
        request_id="demo-request-id"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
