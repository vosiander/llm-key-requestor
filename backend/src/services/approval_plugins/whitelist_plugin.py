"""Whitelist approval plugin."""
import fnmatch
from loguru import logger
from src.services.approval_plugins.base import ApprovalPlugin, ApprovalDecision


class WhitelistApprovalPlugin(ApprovalPlugin):
    """Approval plugin that approves requests matching whitelist patterns."""
    
    def __init__(self):
        """
        Initialize whitelist plugin.
        
        Note:
            Configuration parameters (list) are set after instantiation
            via setattr by the ConfigManager.
        """
        self.list = []
        self.patterns = []
        logger.info(f"WhitelistApprovalPlugin initialized")
    
    def __setattr__(self, name, value):
        """Override setattr to handle 'list' parameter specially."""
        if name == 'list':
            # When 'list' is set, also update 'patterns' for internal use
            super().__setattr__('patterns', value)
            super().__setattr__(name, value)
            logger.info(f"WhitelistApprovalPlugin configured with patterns: {value}")
        else:
            super().__setattr__(name, value)
    
    async def evaluate(self, email: str, model: str, request_id: str) -> ApprovalDecision:
        """
        Evaluate if model matches whitelist patterns.
        
        Args:
            email: User email address
            model: LLM model identifier
            request_id: Request identifier
            
        Returns:
            APPROVE if model matches any whitelist pattern, CONTINUE otherwise
        """
        for pattern in self.patterns:
            if self._matches_pattern(model, pattern):
                logger.info(
                    f"WhitelistApprovalPlugin: APPROVE - model '{model}' matches pattern '{pattern}' "
                    f"for request_id={request_id}"
                )
                return ApprovalDecision.APPROVE
        
        logger.debug(
            f"WhitelistApprovalPlugin: CONTINUE - model '{model}' does not match any whitelist patterns "
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
