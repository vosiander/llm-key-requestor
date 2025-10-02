"""MCP server creation and configuration."""

from mcp.server.fastmcp import FastMCP
from mcp.server.auth.settings import AuthSettings
from loguru import logger
from src.services.kubernetes_secret_service import KubernetesSecretService
from .tools import (
    list_pending_requests,
    list_review_requests,
    approve_request,
    deny_request,
    set_pending,
    set_review,
    request_new_key
)

def create_mcp_server(
    k8s_service: KubernetesSecretService,
    admin_api_key: str
) -> FastMCP:
    """
    Create and configure an MCP server for LLM Key Requestor administration.
    
    Args:
        k8s_service: Kubernetes secret service for managing key requests
        admin_api_key: Admin API key for authentication
        
    Returns:
        Configured FastMCP server instance
    """
    logger.info("Creating MCP server")
    
    mcp = FastMCP(
        name="llm-key-requestor",
        instructions="MCP server for managing LLM API key requests",
        stateless_http=True,
        streamable_http_path="/"
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
    
    logger.info("MCP server created successfully with 7 tools")
    return mcp
