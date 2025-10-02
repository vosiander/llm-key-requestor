"""Email pattern approval plugin."""
import fnmatch
from loguru import logger
from src.services.approval_plugins.base import ApprovalPlugin, ApprovalDecision


class EmailApprovalPlugin(ApprovalPlugin):
    """Approval plugin that approves/denies based on email pattern matching."""
    
    def __init__(self):
        """
        Initialize email plugin.
        
        Note:
            Configuration parameters (pattern) are set after instantiation
            via setattr by the ConfigManager.
        """
        self.pattern = ""
        logger.info(f"EmailApprovalPlugin initialized")
    
    async def evaluate(self, email: str, model: str, request_id: str) -> ApprovalDecision:
        """
        Evaluate if email matches the configured pattern.
        
        Args:
            email: User email address
            model: LLM model identifier
            request_id: Request identifier
            
        Returns:
            APPROVE if email matches pattern, DENY otherwise
        """
        if self._matches_pattern(email, self.pattern):
            logger.info(
                f"EmailApprovalPlugin: APPROVE - email '{email}' matches pattern '{self.pattern}' "
                f"for request_id={request_id}"
            )
            return ApprovalDecision.APPROVE
        
        logger.info(
            f"EmailApprovalPlugin: DENY - email '{email}' does not match pattern '{self.pattern}' "
            f"for request_id={request_id}"
        )
        return ApprovalDecision.DENY
    
    def _matches_pattern(self, email: str, pattern: str) -> bool:
        """
        Check if email matches pattern with wildcard support.
        
        Args:
            email: Email address to check
            pattern: Pattern to match against (supports * and ? wildcards)
            
        Returns:
            True if email matches pattern, False otherwise
        """
        return fnmatch.fnmatch(email, pattern)
