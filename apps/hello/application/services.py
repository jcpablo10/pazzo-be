"""
Application services (Use Cases) for the Hello application.
Contains business logic orchestration.
"""
from __future__ import annotations

from typing import Optional

from ..domain.entities import HelloMessage


class GetHelloMessageUseCase:
    """Use case for generating a hello world message."""

    def __init__(self) -> None:
        """Initialize the use case."""
        pass

    def execute(self, user_email: Optional[str] = None) -> HelloMessage:
        """
        Execute the hello message use case.

        Args:
            user_email: Optional email of the authenticated user

        Returns:
            HelloMessage entity with personalized greeting
        """
        base_message = "Hello World from Pazzo!"

        return HelloMessage(message=base_message, user_email=user_email)
