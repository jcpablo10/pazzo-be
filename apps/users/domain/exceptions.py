"""
Domain exceptions for the Users application.
"""
from __future__ import annotations

from shared.exceptions import DomainException


class UserAlreadyExistsException(DomainException):
    """Raised when attempting to create a user that already exists."""

    def __init__(self, email: str) -> None:
        super().__init__(f"User with email '{email}' already exists")
        self.email = email


class UserNotFoundException(DomainException):
    """Raised when a user cannot be found."""

    def __init__(self, identifier: str) -> None:
        super().__init__(f"User '{identifier}' not found")
        self.identifier = identifier


class InvalidCredentialsException(DomainException):
    """Raised when user credentials are invalid."""

    def __init__(self) -> None:
        super().__init__("Invalid credentials provided")
