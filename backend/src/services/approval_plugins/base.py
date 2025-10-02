"""Base classes and enums for approval plugins."""
from abc import ABC, abstractmethod
from enum import Enum


class ApprovalDecision(str, Enum):
    """Enum for approval plugin decisions."""
    APPROVE = "APPROVE"
    DENY = "DENY"
    CONTINUE = "CONTINUE"
    PENDING = "PENDING"
    REVIEW = "REVIEW"


class ApprovalPlugin(ABC):
    """Abstract base class for approval plugins."""
    
    @abstractmethod
    async def evaluate(self, email: str, model: str, request_id: str) -> ApprovalDecision:
        """
        Evaluate approval request.
        
        Args:
            email: User email address
            model: LLM model identifier
            request_id: Request identifier
            
        Returns:
            ApprovalDecision: APPROVE to immediately approve,
                             DENY to immediately deny,
                             CONTINUE to let next plugin decide
                             REVIEW to mark as pending human review
                             PENDING to mark as pending for later
        """
        pass
