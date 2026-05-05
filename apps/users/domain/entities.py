"""
Domain entities for the Users application.
Pure business logic with no framework dependencies.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class User:
    """
    User domain entity.
    Represents a user in the business domain.
    """

    email: str
    password_hash: str
    is_active: bool = True
    id: Optional[int] = None
    created_at: Optional[datetime] = field(default=None)
    updated_at: Optional[datetime] = field(default=None)

    def verify_password(self, raw_password: str) -> bool:
        """
        Verify if the provided password matches the user's password.

        Args:
            raw_password: The plain text password to verify

        Returns:
            True if password is correct, False otherwise
        """
        from django.contrib.auth.hashers import check_password

        return check_password(raw_password, self.password_hash)

    def is_authenticated(self) -> bool:
        """Check if user is authenticated (active and has valid credentials)."""
        return self.is_active and self.id is not None

    def __str__(self) -> str:
        return f"User(email={self.email}, id={self.id})"
