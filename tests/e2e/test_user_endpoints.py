"""
End-to-end tests for User registration endpoint.
Tests full API flow for user operations.
"""
from __future__ import annotations

from typing import Any

import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.e2e
@pytest.mark.django_db
class TestUserRegistrationEndpoint:
    """Test suite for User Registration API endpoint."""

    def test_register_user_success(self, api_client: APIClient) -> None:
        """Test successful user registration."""
        data = {"email": "newuser@example.com", "password": "securepassword123"}

        response = api_client.post("/api/v1/users/register/", data)

        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data
        assert response.data["email"] == "newuser@example.com"
        assert response.data["is_active"] is True
        assert "password" not in response.data

    def test_register_user_duplicate_email(
        self, api_client: APIClient, create_user: Any, user_data: dict[str, str]
    ) -> None:
        """Test registration with duplicate email fails."""
        response = api_client.post("/api/v1/users/register/", user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_user_invalid_email(self, api_client: APIClient) -> None:
        """Test registration with invalid email fails."""
        data = {"email": "invalid-email", "password": "securepassword123"}

        response = api_client.post("/api/v1/users/register/", data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

    def test_register_user_short_password(self, api_client: APIClient) -> None:
        """Test registration with short password fails."""
        data = {"email": "user@example.com", "password": "short"}

        response = api_client.post("/api/v1/users/register/", data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data

    def test_register_user_missing_email(self, api_client: APIClient) -> None:
        """Test registration without email fails."""
        data = {"password": "securepassword123"}

        response = api_client.post("/api/v1/users/register/", data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

    def test_register_user_missing_password(self, api_client: APIClient) -> None:
        """Test registration without password fails."""
        data = {"email": "user@example.com"}

        response = api_client.post("/api/v1/users/register/", data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data


@pytest.mark.e2e
@pytest.mark.django_db
class TestTokenEndpoint:
    """Test suite for JWT Token endpoints."""

    def test_obtain_token_success(
        self, api_client: APIClient, create_user: Any, user_data: dict[str, str]
    ) -> None:
        """Test obtaining JWT token with valid credentials."""
        response = api_client.post("/api/v1/token/", user_data)

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_obtain_token_invalid_credentials(self, api_client: APIClient) -> None:
        """Test obtaining token with invalid credentials fails."""
        data = {"email": "wrong@example.com", "password": "wrongpassword"}

        response = api_client.post("/api/v1/token/", data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
