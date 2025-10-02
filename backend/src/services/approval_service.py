"""Approval Service for processing key request approvals."""
from loguru import logger
from src.models.key_request import ApprovalResponse, KeyRequestState
from src.services.approval_plugins.base import ApprovalPlugin, ApprovalDecision


class ApprovalService:
    """Service for handling approval workflow using chain-of-responsibility pattern."""
    
    def __init__(self, plugins: list[ApprovalPlugin]):
        """
        Initialize approval service with plugins.
        
        Args:
            plugins: List of approval plugins to evaluate in sequence
        """
        self.plugins = plugins
        logger.info(f"ApprovalService initialized with {len(plugins)} plugins")
    
    async def process(self, email: str, model: str, request_id: str) -> ApprovalResponse:
        """
        Process approval request through plugin chain.
        
        Plugins are evaluated in sequence until one returns APPROVE or DENY.
        If all plugins return CONTINUE, the request is denied by default.
        
        Args:
            email: User email address
            model: LLM model identifier
            request_id: Request identifier
            
        Returns:
            ApprovalResponse with state, reason, and retry flag
        """
        logger.info(f"Processing approval for request_id={request_id}, email={email}, model={model}")
        
        # If no plugins configured, deny by default
        if not self.plugins:
            logger.warning(
                f"No approval plugins configured - denying request_id={request_id}"
            )
            return ApprovalResponse(
                state=KeyRequestState.DENIED,
                reason="No approval plugins configured",
                can_retry=False
            )
        
        for i, plugin in enumerate(self.plugins):
            plugin_name = plugin.__class__.__name__
            logger.debug(
                f"Evaluating plugin {i+1}/{len(self.plugins)}: {plugin_name} "
                f"for request_id={request_id}"
            )
            
            decision = await plugin.evaluate(email, model, request_id)
            logger.debug(f"decision={decision}")
            
            if decision == ApprovalDecision.APPROVE:
                logger.info(
                    f"Request approved by {plugin_name} for request_id={request_id}"
                )
                return ApprovalResponse(
                    state=KeyRequestState.APPROVED,
                    reason=f"Approved by {plugin_name}",
                    can_retry=False
                )

            elif decision == ApprovalDecision.REVIEW:
                logger.info(
                    f"Request marked REVIEW by {plugin_name} for request_id={request_id}"
                )
                return ApprovalResponse(
                    state=KeyRequestState.REVIEW,
                    reason=f"review by {plugin_name}",
                    can_retry=False
                )

            elif decision == ApprovalDecision.PENDING:
                logger.info(
                    f"Request marked PENDING by {plugin_name} for request_id={request_id}"
                )
                return ApprovalResponse(
                    state=KeyRequestState.PENDING,
                    reason=f"Pending by {plugin_name}",
                    can_retry=True
                )
            
            elif decision == ApprovalDecision.DENY:
                logger.info(
                    f"Request denied by {plugin_name} for request_id={request_id}"
                )
                return ApprovalResponse(
                    state=KeyRequestState.DENIED,
                    reason=f"Denied by {plugin_name}",
                    can_retry=False
                )
            
            # decision == ApprovalDecision.CONTINUE, continue to next plugin
            logger.debug(
                f"{plugin_name} returned CONTINUE for request_id={request_id}"
            )
        
        # All plugins returned CONTINUE - deny by default
        logger.info(
            f"All plugins returned CONTINUE - denying request_id={request_id} by default"
        )
        return ApprovalResponse(
            state=KeyRequestState.DENIED,
            reason="All approval plugins returned CONTINUE - denied by default",
            can_retry=False
        )
