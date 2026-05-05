"""
Application ports (interfaces) for the Users application.
Defines contracts for infrastructure implementations.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from ..domain.entities import User


class UserRepository(ABC):
    """
    Repository interface for User entity.
    Defines the contract for User data access.
    """

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        """
        Find a user by their ID.

        Args:
            user_id: The user's unique identifier

        Returns:
            User entity if found, None otherwise
        """
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """
        Find a user by their email address.

        Args:
            email: The user's email address

        Returns:
            User entity if found, None otherwise
        """
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        """
        Save a user (create or update).

        Args:
            user: The user entity to save

        Returns:
            The saved user entity with updated ID
        """
        pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """
        Check if a user exists with the given email.

        Args:
            email: The email to check

        Returns:
            True if user exists, False otherwise
        """
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """
        Delete a user by ID.

        Args:
            user_id: The user's unique identifier

        Returns:
            True if deleted, False if not found
        """
        pass
