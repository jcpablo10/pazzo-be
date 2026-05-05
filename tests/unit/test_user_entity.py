"""
Unit tests for User domain entities.
These tests have no Django dependencies.
"""
from __future__ import annotations

import pytest
from django.contrib.auth.hashers import make_password

from apps.users.domain.entities import User


@pytest.mark.unit
class TestUserEntity:
    """Test suite for User entity."""

    def test_create_user(self) -> None:
        """Test creating a user entity."""
        user = User(
            email="test@example.com",
            password_hash=make_password("password123"),
            is_active=True,
        )

        assert user.email == "test@example.com"
        assert user.is_active is True
        assert user.id is None

    def test_verify_password_success(self) -> None:
        """Test password verification with correct password."""
        user = User(
            email="test@example.com",
            password_hash=make_password("password123"),
            is_active=True,
        )

        assert user.verify_password("password123") is True

    def test_verify_password_failure(self) -> None:
        """Test password verification with incorrect password."""
        user = User(
            email="test@example.com",
            password_hash=make_password("password123"),
            is_active=True,
        )

        assert user.verify_password("wrongpassword") is False

    def test_is_authenticated_active_user_with_id(self) -> None:
        """Test is_authenticated for active user with ID."""
        user = User(
            id=1,
            email="test@example.com",
            password_hash=make_password("password123"),
            is_active=True,
        )

        assert user.is_authenticated() is True

    def test_is_authenticated_inactive_user(self) -> None:
        """Test is_authenticated for inactive user."""
        user = User(
            id=1,
            email="test@example.com",
            password_hash=make_password("password123"),
            is_active=False,
        )

        assert user.is_authenticated() is False

    def test_is_authenticated_user_without_id(self) -> None:
        """Test is_authenticated for user without ID."""
        user = User(
            email="test@example.com",
            password_hash=make_password("password123"),
            is_active=True,
        )

        assert user.is_authenticated() is False

    def test_string_representation(self) -> None:
        """Test string representation of User."""
        user = User(
            id=1,
            email="test@example.com",
            password_hash=make_password("password123"),
        )

        assert str(user) == "User(email=test@example.com, id=1)"
