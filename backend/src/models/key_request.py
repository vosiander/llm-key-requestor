"""Pydantic models for key request system."""
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class KeyRequestState(str, Enum):
    """Enum for key request states"""
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    REVIEW = "in-review"


class ApprovalResponse(BaseModel):
    """Response from approval service"""
    state: KeyRequestState
    reason: str
    can_retry: bool


class KeyRequestData(BaseModel):
    """Data stored in Kubernetes secret"""
    request_id: str
    email: EmailStr
    model: str
    state: KeyRequestState
    created_at: datetime
    updated_at: datetime
    api_key: Optional[str] = None


class EmailConfig(BaseModel):
    """SMTP configuration for email service"""
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    smtp_from: str
    smtp_use_tls: bool = True
