"""Background queue processor for handling pending key requests."""
import asyncio
import re
from typing import Optional
from loguru import logger
from injector import inject
from config import config_manager
from src.services.kubernetes_secret_service import KubernetesSecretService
from src.services.approval_service import ApprovalService
from src.models.key_request import KeyRequestState, KeyRequestData

class QueueProcessor:
    """Background task processor for pending key requests."""
    
    @inject
    def __init__(
        self,
        k8s_service: KubernetesSecretService,
        approval_service: ApprovalService
    ):
        """
        Initialize queue processor with required services.
        
        Args:
            k8s_service: Kubernetes secret service
            approval_service: Approval service
        """
        self.k8s_service = k8s_service
        self.approval_service = approval_service
        self.running = False
        self.task: Optional[asyncio.Task] = None
        
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
            approval_response = await self.approval_service.process(
                email=request.email,
                model=request.model,
                request_id=request.request_id
            )
            
            # Take action based on decision
            await self.approval_service.take_action(approval_response, request)
            
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
