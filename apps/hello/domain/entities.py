"""
Domain entities for the Hello application.
Pure business logic with no framework dependencies.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class HelloMessage:
    """
    HelloMessage domain entity.
    Represents a greeting message in the business domain.
    """

    message: str
    user_email: Optional[str] = None
    timestamp: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Initialize timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def get_full_message(self) -> str:
        """
        Get the complete message with user information.

        Returns:
            Formatted greeting message
        """
        if self.user_email:
            return f"{self.message} Welcome, {self.user_email}!"
        return self.message

    def __str__(self) -> str:
        return self.get_full_message()
