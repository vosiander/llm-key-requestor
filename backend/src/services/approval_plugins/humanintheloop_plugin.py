"""HumanInTheLoop approval plugin."""
import fnmatch
from loguru import logger
from src.services.approval_plugins.base import ApprovalPlugin, ApprovalDecision
from injector import inject

from src.services.email_service import EmailService


class HumanintheloopApprovalPlugin(ApprovalPlugin):
    """Approval plugin that denies requests matching HumanInTheLoop patterns."""

    @inject
    def __init__(self, email_service: EmailService):
        """
        Initialize HumanInTheLoop plugin.
        
        Args:
            email_service: EmailService instance for sending notifications (injected)
        
        Note:
            Configuration parameters (email, patterns) are set after instantiation
            via setattr by the ConfigManager.
        """
        self.email_service = email_service
        self.email = None
        self.patterns = []
        logger.info(f"HumanInTheLoopApprovalPlugin initialized")
    
    async def evaluate(self, email: str, model: str, request_id: str) -> ApprovalDecision:
        """
        Evaluate if model matches HumanInTheLoop patterns.
        
        Args:
            email: User email address
            model: LLM model identifier
            request_id: Request identifier
            
        Returns:
            DENY if model matches any HumanInTheLoop pattern, CONTINUE otherwise
        """
        logger.info(f"HumanInTheLoopApprovalPlugin evaluate for {email}, {model} and patterns {self.patterns}")
        for pattern in self.patterns:
            if self._matches_pattern(model, pattern):
                logger.info(f"Model is marked for human review: '{model}' matches pattern '{pattern}' ")
                if self.email is not None:
                    request = f"""
A request was made for a model that requires human approval.
Please review and approve or deny the request.

Request ID: {request_id}
Model: {model}
User Email: {email}
                    """
                    await self.email_service.notify(self.email, request)
                return ApprovalDecision.REVIEW

        logger.debug(
            f"HumanInTheLoopApprovalPlugin: CONTINUE - model '{model}' does not match any HumanInTheLoop patterns "
            f"for request_id={request_id}"
        )
        return ApprovalDecision.CONTINUE
    
    def _matches_pattern(self, model: str, pattern: str) -> bool:
        """
        Check if model matches pattern with wildcard support.
        
        Args:
            model: Model identifier to check
            pattern: Pattern to match against (supports * and ? wildcards)
            
        Returns:
            True if model matches pattern, False otherwise
        """
        return fnmatch.fnmatch(model, pattern)
