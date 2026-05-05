"""
Data Transfer Objects (DTOs) for the Users application.
Used to transfer data between layers.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class UserInputDTO:
    """DTO for user input data (registration, updates)."""

    email: str
    password: str


@dataclass
class UserOutputDTO:
    """DTO for user output data (API responses)."""

    id: int
    email: str
    is_active: bool
    created_at: Optional[datetime] = None

    @classmethod
    def from_entity(cls, user: Any) -> UserOutputDTO:
        """
        Create a UserOutputDTO from a User entity.

        Args:
            user: User entity

        Returns:
            UserOutputDTO instance
        """
        from ..domain.entities import User

        if isinstance(user, User):
            return cls(
                id=user.id or 0,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
            )
        raise ValueError("Invalid user entity")


from typing import Any
