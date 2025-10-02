"""MCP tools for managing LLM key requests."""

from datetime import datetime
from loguru import logger
from mcp.server.fastmcp import Context

from src.models.key_request import KeyRequestState
from src.services.kubernetes_secret_service import KubernetesSecretService

async def list_pending_requests(ctx: Context, k8s_service: KubernetesSecretService) -> list[dict]:
    """
    List all key requests in PENDING state.
    
    Requires admin authentication.
    
    Args:
        ctx: MCP context for authentication
        k8s_service: Service for accessing Kubernetes secrets
        
    Returns:
        List of pending key requests with their details
    """
    logger.info("Listing pending key requests")
    
    try:
        pending_requests = await k8s_service.find_by_status(KeyRequestState.PENDING)
        
        result = [
            {
                "request_id": req.request_id,
                "email": req.email,
                "model": req.model,
                "state": req.state.value,
                "created_at": req.created_at.isoformat(),
                "updated_at": req.updated_at.isoformat()
            }
            for req in pending_requests
        ]
        
        logger.info(f"Found {len(result)} pending requests")
        return result
        
    except Exception as e:
        logger.error(f"Error listing pending requests: {e}", exc_info=True)
        raise


async def list_review_requests(ctx: Context, k8s_service: KubernetesSecretService) -> list[dict]:
    """
    List all key requests in REVIEW state.
    
    Requires admin authentication.
    
    Args:
        ctx: MCP context for authentication
        k8s_service: Service for accessing Kubernetes secrets
        
    Returns:
        List of key requests in review with their details
    """
    logger.info("Listing review key requests")
    
    try:
        review_requests = await k8s_service.find_by_status(KeyRequestState.REVIEW)
        
        result = [
            {
                "request_id": req.request_id,
                "email": req.email,
                "model": req.model,
                "state": req.state.value,
                "created_at": req.created_at.isoformat(),
                "updated_at": req.updated_at.isoformat()
            }
            for req in review_requests
        ]
        
        logger.info(f"Found {len(result)} review requests")
        return result
        
    except Exception as e:
        logger.error(f"Error listing review requests: {e}", exc_info=True)
        raise


async def approve_request(ctx: Context, request_id: str, k8s_service: KubernetesSecretService) -> dict:
    """
    Approve a key request by changing its state to APPROVED.
    
    Requires admin authentication.
    
    Args:
        ctx: MCP context for authentication
        request_id: The ID of the request to approve
        k8s_service: Service for accessing Kubernetes secrets
        
    Returns:
        Updated request details
    """
    logger.info(f"Approving request: {request_id}")
    
    try:
        # Find the request
        request = await k8s_service.find(request_id)
        if not request:
            raise ValueError(f"Request not found: {request_id}")
        
        # Update state to APPROVED
        request.state = KeyRequestState.APPROVED
        request.updated_at = datetime.now()
        
        # Save the updated request
        await k8s_service.update(request.request_id, state=request.state, updated_at=request.updated_at)

        result = {
            "request_id": request.request_id,
            "email": request.email,
            "model": request.model,
            "state": request.state.value,
            "updated_at": request.updated_at.isoformat()
        }
        
        logger.info(f"Request {request_id} approved successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error approving request {request_id}: {e}", exc_info=True)
        raise


async def deny_request(ctx: Context, request_id: str, k8s_service: KubernetesSecretService) -> dict:
    """
    Deny a key request by changing its state to DENIED.
    
    Requires admin authentication.
    
    Args:
        ctx: MCP context for authentication
        request_id: The ID of the request to deny
        k8s_service: Service for accessing Kubernetes secrets
        
    Returns:
        Updated request details
    """
    logger.info(f"Denying request: {request_id}")
    
    try:
        # Find the request
        request = await k8s_service.find(request_id)
        if not request:
            raise ValueError(f"Request not found: {request_id}")
        
        # Update state to DENIED
        request.state = KeyRequestState.DENIED
        request.updated_at = datetime.now()
        
        # Save the updated request
        await k8s_service.update(request.request_id, state=request.state, updated_at=request.updated_at)
        
        result = {
            "request_id": request.request_id,
            "email": request.email,
            "model": request.model,
            "state": request.state.value,
            "updated_at": request.updated_at.isoformat()
        }
        
        logger.info(f"Request {request_id} denied successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error denying request {request_id}: {e}", exc_info=True)
        raise


async def set_pending(ctx: Context, request_id: str, k8s_service: KubernetesSecretService) -> dict:
    """
    Set a key request state to PENDING.
    
    Requires admin authentication.
    
    Args:
        ctx: MCP context for authentication
        request_id: The ID of the request to set to pending
        k8s_service: Service for accessing Kubernetes secrets
        
    Returns:
        Updated request details
    """
    logger.info(f"Setting request to pending: {request_id}")
    
    try:
        # Find the request
        request = await k8s_service.find(request_id)
        if not request:
            raise ValueError(f"Request not found: {request_id}")
        
        # Update state to PENDING
        request.state = KeyRequestState.PENDING
        request.updated_at = datetime.now()

        # Save the updated request
        await k8s_service.update(request.request_id, state=request.state, updated_at=request.updated_at)
        
        result = {
            "request_id": request.request_id,
            "email": request.email,
            "model": request.model,
            "state": request.state.value,
            "updated_at": request.updated_at.isoformat()
        }
        
        logger.info(f"Request {request_id} set to pending successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error setting request {request_id} to pending: {e}", exc_info=True)
        raise


async def set_review(ctx: Context, request_id: str, k8s_service: KubernetesSecretService) -> dict:
    """
    Set a key request state to REVIEW.
    
    Requires admin authentication.
    
    Args:
        ctx: MCP context for authentication
        request_id: The ID of the request to set to review
        k8s_service: Service for accessing Kubernetes secrets
        
    Returns:
        Updated request details
    """
    logger.info(f"Setting request to review: {request_id}")
    
    try:
        # Find the request
        request = await k8s_service.find(request_id)
        if not request:
            raise ValueError(f"Request not found: {request_id}")
        
        # Update state to REVIEW
        request.state = KeyRequestState.REVIEW
        request.updated_at = datetime.now()
        
        # Save the updated request
        await k8s_service.update(request.request_id, state=request.state, updated_at=request.updated_at)
        
        result = {
            "request_id": request.request_id,
            "email": request.email,
            "model": request.model,
            "state": request.state.value,
            "updated_at": request.updated_at.isoformat()
        }
        
        logger.info(f"Request {request_id} set to review successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error setting request {request_id} to review: {e}", exc_info=True)
        raise


async def request_new_key(email: str, model: str, k8s_service: KubernetesSecretService) -> dict:
    """
    Create a new key request.
    
    This tool does not require authentication and can be used by anyone.
    
    Args:
        email: Email address for the request
        model: Model identifier
        k8s_service: Service for accessing Kubernetes secrets
        
    Returns:
        Created request details
    """
    logger.info(f"Creating new key request for {email}, model: {model}")
    
    try:
        # Create new request
        request = await k8s_service.create(email=email, model=model)
        
        result = {
            "request_id": request.request_id,
            "email": request.email,
            "model": request.model,
            "state": request.state.value,
            "created_at": request.created_at.isoformat(),
            "updated_at": request.updated_at.isoformat()
        }
        
        logger.info(f"Request created successfully: {request.request_id}")
        return result
        
    except Exception as e:
        logger.error(f"Error creating key request for {email}: {e}", exc_info=True)
        raise
