"""Background queue processor for handling pending key requests."""
import asyncio
import logging
import re
from typing import Optional
from loguru import logger
from config import config_manager
from src.services.kubernetes_secret_service import KubernetesSecretService
from src.services.approval_service import ApprovalService
from src.services.email_service import EmailService
from src.litellm.manager import KeyManagement
from src.models.key_request import KeyRequestState, KeyRequestData

class QueueProcessor:
    """Background task processor for pending key requests."""
    
    def __init__(
        self,
        k8s_service: KubernetesSecretService,
        approval_service: ApprovalService,
        email_service: EmailService,
        key_manager: KeyManagement
    ):
        """
        Initialize queue processor with required services.
        
        Args:
            k8s_service: Kubernetes secret service
            approval_service: Approval service
            email_service: Email notification service
            key_manager: LiteLLM key management service
        """
        self.k8s_service = k8s_service
        self.approval_service = approval_service
        self.email_service = email_service
        self.key_manager = key_manager
        self.running = False
        self.task: Optional[asyncio.Task] = None
        
        # Get LiteLLM configuration
        self.litellm_config = config_manager.get_litellm_config()
        
        logger.info("QueueProcessor initialized")
    
    def parse_interval(self, interval_str: str) -> int:
        """
        Parse interval string to seconds.
        
        Supports formats: "30s", "1m", "5m", etc.
        
        Args:
            interval_str: Interval string (e.g., "30s", "1m")
            
        Returns:
            Interval in seconds
        """
        match = re.match(r'^(\d+)([smh])$', interval_str.lower())
        if not match:
            logger.warning(f"Invalid interval format: {interval_str}, defaulting to 30s")
            return 30
        
        value, unit = match.groups()
        value = int(value)
        
        if unit == 's':
            return value
        elif unit == 'm':
            return value * 60
        elif unit == 'h':
            return value * 3600
        
        return 30
    
    async def process_single_request(self, request: KeyRequestData) -> None:
        """
        Process a single pending request.
        
        Args:
            request: KeyRequestData to process
        """
        try:
            logger.info(f"Processing request {request.request_id} for {request.email}")
            
            # Get approval decision
            approval_response = await self.approval_service.approve(
                email=request.email,
                model=request.model,
                request_id=request.request_id
            )

            key_alias = f"user-{request.email}-{request.model}"

            logger.info(
                f"Approval response for {request.request_id} {key_alias}: "
                f"state={approval_response.state.value}, reason={approval_response.reason}"
            )
            
            # Handle approval response based on state
            if approval_response.state == KeyRequestState.APPROVED:
                # Generate API key using LiteLLM
                try:
                    self.key_manager.delete_key(
                        litellm_host=self.litellm_config.base_url,
                        litellm_api_key=self.litellm_config.api_key,
                        key_alias=key_alias,
                    )
                    logger.info(f"deleted API key for request {request.request_id}")

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
                        gateway_url=self.litellm_config.base_url
                    )

                    logger.info(f"Email sent: {email_sent}")

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
                # Still pending, continue to next request
                logger.info(f"Request {request.request_id} still pending, will retry in next cycle")
            
        except Exception as e:
            logger.error(f"Error processing request {request.request_id}: {e}", exc_info=True)
    
    async def process_queue(self) -> None:
        """Main queue processing loop."""
        interval_str = config_manager.get_queue_interval()
        interval_seconds = self.parse_interval(interval_str)
        
        logger.info(f"Starting queue processor with interval {interval_str} ({interval_seconds}s)")
        
        while self.running:
            try:
                # Get all pending requests
                pending_requests = await self.k8s_service.find_by_status(KeyRequestState.PENDING)
                
                if pending_requests:
                    logger.info(f"Found {len(pending_requests)} pending request(s) to process")
                    
                    # Process each pending request
                    for request in pending_requests:
                        if not self.running:
                            break
                        await self.process_single_request(request)
                else:
                    logger.debug("No pending requests to process")
                
            except Exception as e:
                logger.error(f"Error in queue processing cycle: {e}", exc_info=True)
            
            # Wait for next cycle
            await asyncio.sleep(interval_seconds)
        
        logger.info("Queue processor stopped")
    
    def start(self) -> None:
        """Start the queue processor background task."""
        if self.running:
            logger.warning("Queue processor is already running")
            return
        
        self.running = True
        self.task = asyncio.create_task(self.process_queue())
        logger.info("Queue processor started")
    
    async def stop(self) -> None:
        """Stop the queue processor background task."""
        if not self.running:
            logger.warning("Queue processor is not running")
            return
        
        logger.info("Stopping queue processor...")
        self.running = False
        
        if self.task:
            # Wait for current cycle to complete (with timeout)
            try:
                await asyncio.wait_for(self.task, timeout=10.0)
            except asyncio.TimeoutError:
                logger.warning("Queue processor did not stop gracefully, cancelling task")
                self.task.cancel()
                try:
                    await self.task
                except asyncio.CancelledError:
                    pass
        
        logger.info("Queue processor stopped")
