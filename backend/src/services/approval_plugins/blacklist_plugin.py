"""Blacklist approval plugin."""
import fnmatch
from loguru import logger
from src.services.approval_plugins.base import ApprovalPlugin, ApprovalDecision


class BlacklistApprovalPlugin(ApprovalPlugin):
    """Approval plugin that denies requests matching blacklist patterns."""
    
    def __init__(self):
        """
        Initialize blacklist plugin.
        
        Note:
            Configuration parameters (list) are set after instantiation
            via setattr by the ConfigManager.
        """
        self.list = []
        self.patterns = []
        logger.info(f"BlacklistApprovalPlugin initialized")
    
    def __setattr__(self, name, value):
        """Override setattr to handle 'list' parameter specially."""
        if name == 'list':
            # When 'list' is set, also update 'patterns' for internal use
            super().__setattr__('patterns', value)
            super().__setattr__(name, value)
            logger.info(f"BlacklistApprovalPlugin configured with patterns: {value}")
        else:
            super().__setattr__(name, value)
    
    async def evaluate(self, email: str, model: str, request_id: str) -> ApprovalDecision:
        """
        Evaluate if model matches blacklist patterns.
        
        Args:
            email: User email address
            model: LLM model identifier
            request_id: Request identifier
            
        Returns:
            DENY if model matches any blacklist pattern, CONTINUE otherwise
        """
        for pattern in self.patterns:
            if self._matches_pattern(model, pattern):
                logger.info(
                    f"BlacklistApprovalPlugin: DENY - model '{model}' matches pattern '{pattern}' "
                    f"for request_id={request_id}"
                )
                return ApprovalDecision.DENY
        
        logger.debug(
            f"BlacklistApprovalPlugin: CONTINUE - model '{model}' does not match any blacklist patterns "
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
