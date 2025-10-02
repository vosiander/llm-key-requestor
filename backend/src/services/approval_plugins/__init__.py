"""Approval plugins package for plugin-based approval system."""
from src.services.approval_plugins.base import ApprovalDecision, ApprovalPlugin

__all__ = ["ApprovalDecision", "ApprovalPlugin"]
