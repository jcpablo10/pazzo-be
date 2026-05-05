"""
Integration tests for User repository.
Tests database interactions.
"""
from __future__ import annotations

import pytest
from django.contrib.auth.hashers import make_password

from apps.users.domain.entities import User
from apps.users.infrastructure.repositories import DjangoUserRepository


@pytest.mark.integration
@pytest.mark.django_db
class TestDjangoUserRepository:
    """Test suite for DjangoUserRepository."""

    def test_save_new_user(self) -> None:
        """Test saving a new user to database."""
        repository = DjangoUserRepository()
        user = User(
            email="newuser@example.com",
            password_hash=make_password("password123"),
            is_active=True,
        )

        saved_user = repository.save(user)

        assert saved_user.id is not None
        assert saved_user.email == "newuser@example.com"
        assert saved_user.is_active is True

    def test_find_by_email_existing_user(self) -> None:
        """Test finding an existing user by email."""
        repository = DjangoUserRepository()
        user = User(
            email="findme@example.com",
            password_hash=make_password("password123"),
            is_active=True,
        )
        repository.save(user)

        found_user = repository.find_by_email("findme@example.com")

        assert found_user is not None
        assert found_user.email == "findme@example.com"

    def test_find_by_email_nonexistent_user(self) -> None:
        """Test finding a non-existent user by email."""
        repository = DjangoUserRepository()

        found_user = repository.find_by_email("notfound@example.com")

        assert found_user is None

    def test_exists_by_email_true(self) -> None:
        """Test exists_by_email returns True for existing user."""
        repository = DjangoUserRepository()
        user = User(
            email="exists@example.com",
            password_hash=make_password("password123"),
            is_active=True,
        )
        repository.save(user)

        exists = repository.exists_by_email("exists@example.com")

        assert exists is True

    def test_exists_by_email_false(self) -> None:
        """Test exists_by_email returns False for non-existent user."""
        repository = DjangoUserRepository()

        exists = repository.exists_by_email("doesnotexist@example.com")

        assert exists is False

    def test_delete_user(self) -> None:
        """Test deleting a user."""
        repository = DjangoUserRepository()
        user = User(
            email="deleteme@example.com",
            password_hash=make_password("password123"),
            is_active=True,
        )
        saved_user = repository.save(user)

        assert saved_user.id is not None
        deleted = repository.delete(saved_user.id)

        assert deleted is True
        assert repository.find_by_email("deleteme@example.com") is None
