"""
End-to-end tests for Hello World endpoint.
Tests full API flow with authentication.
"""
from __future__ import annotations

from typing import Any

import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.e2e
@pytest.mark.django_db
class TestHelloWorldEndpoint:
    """Test suite for Hello World API endpoint."""

    def test_hello_without_authentication_returns_401(
        self, api_client: APIClient
    ) -> None:
        """Test that accessing /hello/ without auth returns 401."""
        response = api_client.get("/api/v1/hello/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_hello_with_valid_token_returns_200(
        self, authenticated_client: APIClient, create_user: Any
    ) -> None:
        """Test that accessing /hello/ with valid token returns 200."""
        response = authenticated_client.get("/api/v1/hello/")

        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.data
        assert response.data["message"] == "Hello World from Pazzo!"

    def test_hello_includes_user_email(
        self, authenticated_client: APIClient, create_user: Any
    ) -> None:
        """Test that response includes authenticated user's email."""
        response = authenticated_client.get("/api/v1/hello/")

        assert response.status_code == status.HTTP_200_OK
        assert "user" in response.data
        assert response.data["user"] == create_user.email

    def test_hello_includes_timestamp(
        self, authenticated_client: APIClient, create_user: Any
    ) -> None:
        """Test that response includes timestamp."""
        response = authenticated_client.get("/api/v1/hello/")

        assert response.status_code == status.HTTP_200_OK
        assert "timestamp" in response.data
        assert response.data["timestamp"] is not None

    def test_hello_with_invalid_token_returns_401(
        self, api_client: APIClient
    ) -> None:
        """Test that accessing /hello/ with invalid token returns 401."""
        api_client.credentials(HTTP_AUTHORIZATION="Bearer invalid_token_here")
        response = api_client.get("/api/v1/hello/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
