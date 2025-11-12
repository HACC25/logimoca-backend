"""Client-side models for request/response validation."""

from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator

class ClientModel(BaseModel):
    """Base class for client-side models."""
    session_id: str = Field(..., description="Unique session identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completion_time_seconds: int = Field(..., description="Time taken to complete assessment")

    @field_validator("session_id")
    def validate_session_id(cls, v: str) -> str:
        """Validate session ID format."""
        if not v or len(v) < 8:
            raise ValueError("Session ID must be at least 8 characters")
        return v

    @field_validator("completion_time_seconds")
    def validate_completion_time(cls, v: int) -> int:
        """Validate completion time."""
        if v <= 0:
            raise ValueError("Completion time must be positive")
        return v