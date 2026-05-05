"""
Repository implementations for the Users application.
Infrastructure layer - data access.
"""
from __future__ import annotations

from typing import Optional

from ..application.ports import UserRepository
from ..domain.entities import User
from .models import UserModel


class DjangoUserRepository(UserRepository):
    """
    Django ORM implementation of UserRepository.
    Handles conversion between ORM models and domain entities.
    """

    def find_by_id(self, user_id: int) -> Optional[User]:
        """Find a user by ID."""
        try:
            user_model = UserModel.objects.get(id=user_id)
            return self._to_entity(user_model)
        except UserModel.DoesNotExist:
            return None

    def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by email."""
        try:
            user_model = UserModel.objects.get(email=email)
            return self._to_entity(user_model)
        except UserModel.DoesNotExist:
            return None

    def save(self, user: User) -> User:
        """Save (create or update) a user."""
        if user.id:
            # Update existing user
            user_model = UserModel.objects.get(id=user.id)
            user_model.email = user.email
            user_model.password_hash = user.password_hash
            user_model.is_active = user.is_active
            user_model.save()
        else:
            # Create new user
            user_model = UserModel.objects.create(
                email=user.email,
                password_hash=user.password_hash,
                is_active=user.is_active,
            )

        return self._to_entity(user_model)

    def exists_by_email(self, email: str) -> bool:
        """Check if a user exists with the given email."""
        return UserModel.objects.filter(email=email).exists()

    def delete(self, user_id: int) -> bool:
        """Delete a user by ID."""
        try:
            user_model = UserModel.objects.get(id=user_id)
            user_model.delete()
            return True
        except UserModel.DoesNotExist:
            return False

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        """
        Convert ORM model to domain entity.

        Args:
            model: UserModel instance

        Returns:
            User domain entity
        """
        return User(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
