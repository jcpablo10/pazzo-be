"""
Shared exceptions for the Pazzo application.
"""
from __future__ import annotations


class PazzoException(Exception):
    """Base exception for all Pazzo application errors."""

    def __init__(self, message: str = "An error occurred") -> None:
        self.message = message
        super().__init__(self.message)


class DomainException(PazzoException):
    """Exception for domain layer errors."""

    pass


class ApplicationException(PazzoException):
    """Exception for application layer errors."""

    pass


class InfrastructureException(PazzoException):
    """Exception for infrastructure layer errors."""

    pass
