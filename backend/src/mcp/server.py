"""MCP server creation and configuration."""

from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
from loguru import logger
from config import config_manager
from src.services.kubernetes_secret_service import KubernetesSecretService
from .tools import (
    list_pending_requests,
    list_review_requests,
    approve_request,
    deny_request,
    set_pending,
    set_review,
    request_new_key,
    get_available_models
)

def create_mcp_server(k8s_service: KubernetesSecretService,) -> FastMCP:
    """
    Create and configure an MCP server for LLM Key Requestor administration.
    
    Args:
        k8s_service: Kubernetes secret service for managing key requests

    Returns:
        Configured FastMCP server instance
    """
    logger.info("Creating MCP server")
    
    # Get MCP configuration for API key
    mcp_config = config_manager.get_mcp_config()
    
    # Require API key for security
    if not mcp_config.api_key:
        error_msg = (
            "No API key configured for MCP server. "
            "Please set 'mcp.api_key' in config.yaml or MCP_API_KEY environment variable."
        )
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    logger.info("Configuring MCP server with API key authentication")
    # StaticTokenVerifier accepts tokens as a dict with token -> claims mapping
    # For simple API key auth, we use a single token with basic client_id
    auth_provider = StaticTokenVerifier(
        tokens={
            mcp_config.api_key: {
                "client_id": "admin",
                "scopes": ["admin"]
            }
        }
    )
    
    mcp = FastMCP(
        name="llm-key-requestor",
        instructions="MCP server for managing LLM API key requests",
        stateless_http=True,
        streamable_http_path="/",
        auth=auth_provider
    )

    @mcp.tool()
    async def list_pending(ctx) -> list[dict]:
        """List all key requests in PENDING state. Requires admin authentication."""
        return await list_pending_requests(ctx, k8s_service)
    
    @mcp.tool()
    async def list_review(ctx) -> list[dict]:
        """List all key requests in REVIEW state. Requires admin authentication."""
        return await list_review_requests(ctx, k8s_service)
    
    @mcp.tool()
    async def approve(ctx, request_id: str) -> dict:
        """Approve a key request by ID. Requires admin authentication."""
        return await approve_request(ctx, request_id, k8s_service)
    
    @mcp.tool()
    async def deny(ctx, request_id: str) -> dict:
        """Deny a key request by ID. Requires admin authentication."""
        return await deny_request(ctx, request_id, k8s_service)
    
    @mcp.tool()
    async def pending(ctx, request_id: str) -> dict:
        """Set a key request to PENDING state by ID. Requires admin authentication."""
        return await set_pending(ctx, request_id, k8s_service)
    
    @mcp.tool()
    async def review(ctx, request_id: str) -> dict:
        """Set a key request to REVIEW state by ID. Requires admin authentication."""
        return await set_review(ctx, request_id, k8s_service)
    
    @mcp.tool()
    async def request_key(email: str, model: str) -> dict:
        """Create a new key request. Does not require authentication."""
        return await request_new_key(email, model, k8s_service)
    
    @mcp.tool()
    def list_models() -> list[dict]:
        """Get list of available LLM models with metadata. Does not require authentication."""
        return get_available_models()
    
    logger.info("MCP server created successfully with 8 tools")
    return mcp
