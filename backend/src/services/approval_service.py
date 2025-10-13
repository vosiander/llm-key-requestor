"""Approval Service for processing key request approvals."""
from typing import List
from loguru import logger
from src.models.key_request import ApprovalResponse, KeyRequestState, KeyRequestData
from src.services.approval_plugins.base import ApprovalPlugin, ApprovalDecision
from src.services.kubernetes_secret_service import KubernetesSecretService
from src.services.email_service import EmailService
from src.litellm.manager import KeyManagement


class ApprovalService:
    """Service for handling approval workflow using chain-of-responsibility pattern."""
    
    def __init__(
        self,
        plugins: List[ApprovalPlugin],
        k8s_service: KubernetesSecretService,
        email_service: EmailService,
        key_manager: KeyManagement,
        litellm_config: dict,
    ):
        """
        Initialize approval service with plugins and dependencies.
        
        Args:
            plugins: List of approval plugins to evaluate in sequence
            k8s_service: Kubernetes secret service for state updates
            email_service: Email service for notifications
            key_manager: LiteLLM key management service
            litellm_config: LiteLLM configuration
        """
        self.plugins = plugins
        self.k8s_service = k8s_service
        self.email_service = email_service
        self.key_manager = key_manager
        self.litellm_config = litellm_config
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
    
    async def take_action(self, approval_response: ApprovalResponse, request: KeyRequestData) -> None:
        """
        Execute actions based on approval decision.
        
        Args:
            approval_response: The decision from the process() method
            request: The key request data to process
        """
        key_alias = f"user-{request.email}-{request.model}"
        
        logger.info(
            f"Taking action for {request.request_id} {key_alias}: "
            f"state={approval_response.state.value}, reason={approval_response.reason}"
        )
        
        try:
            if approval_response.state == KeyRequestState.APPROVED:
                # Generate API key using LiteLLM
                try:
                    # Delete existing key if any
                    self.key_manager.delete_key(
                        litellm_host=self.litellm_config.base_url,
                        litellm_api_key=self.litellm_config.api_key,
                        key_alias=key_alias,
                    )
                    logger.info(f"Deleted existing API key for request {request.request_id}")

                    # Generate new key
                    api_key = self.key_manager.generate_key(
                        litellm_host=self.litellm_config.base_url,
                        litellm_api_key=self.litellm_config.api_key,
                        user_id=request.email,
                        key_alias=key_alias,
                        key_name=f"{request.email} - {request.model}",
                        models=[request.model]
                    )
                    
                    logger.info(f"Generated API key for request {request.request_id}")
                    
                    # Send approval email with API key
                    email_sent = await self.email_service.send_approval_notification(
                        email=request.email,
                        model=request.model,
                        api_key=api_key,
                        gateway_url=self.litellm_config.gateway_url
                    )

                    if email_sent:
                        logger.info(f"Approval notification sent to {request.email}")
                    else:
                        logger.warning(f"Failed to send approval notification to {request.email}")

                    # Update secret with approved state and API key
                    await self.k8s_service.update(
                        request.request_id,
                        state=KeyRequestState.APPROVED,
                        api_key=api_key
                    )
                    
                except Exception as e:
                    logger.error(f"Error generating API key for {request.request_id}: {e}", exc_info=True)
                    # Update to denied state on key generation failure
                    await self.k8s_service.update(
                        request.request_id,
                        state=KeyRequestState.DENIED
                    )
                    
                    # Send denial email
                    await self.email_service.send_denial_notification(
                        email=request.email,
                        model=request.model,
                        reason=f"Failed to generate API key: {str(e)}"
                    )
            
            elif approval_response.state == KeyRequestState.DENIED:
                # Update to denied state
                await self.k8s_service.update(
                    request.request_id,
                    state=KeyRequestState.DENIED
                )
                
                # Send denial email
                email_sent = await self.email_service.send_denial_notification(
                    email=request.email,
                    model=request.model,
                    reason=approval_response.reason
                )
                
                if email_sent:
                    logger.info(f"Denial notification sent to {request.email}")
                else:
                    logger.warning(f"Failed to send denial notification to {request.email}")
            
            elif approval_response.state == KeyRequestState.PENDING:
                # Still pending, will retry in next cycle
                logger.info(f"Request {request.request_id} still pending, will retry in next cycle")

            elif approval_response.state == KeyRequestState.REVIEW:
                # Update secret with review state
                await self.k8s_service.update(
                    request.request_id,
                    state=KeyRequestState.REVIEW,
                )
                logger.info(f"Request {request.request_id} marked for review")
                
        except Exception as e:
            logger.error(f"Error taking action for request {request.request_id}: {e}", exc_info=True)
