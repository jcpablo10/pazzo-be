"""
Pytest configuration and fixtures for Pazzo tests.
"""
from __future__ import annotations

from typing import Any, TYPE_CHECKING

import pytest
from rest_framework.test import APIClient

if TYPE_CHECKING:
    from apps.users.domain.entities import User


@pytest.fixture
def api_client() -> APIClient:
    """
    Fixture for Django REST Framework API client.

    Returns:
        APIClient instance for making test requests
    """
    return APIClient()


@pytest.fixture
def user_data() -> dict[str, str]:
    """
    Fixture for sample user data.

    Returns:
        Dictionary with user credentials
    """
    return {"email": "test@example.com", "password": "testpassword123"}


@pytest.fixture
@pytest.mark.django_db
def create_user(user_data: dict[str, str]) -> Any:
    """
    Fixture to create a test user.

    Args:
        user_data: User credentials dictionary

    Returns:
        Created UserModel instance
    """
    from apps.users.infrastructure.models import UserModel
    from django.contrib.auth.hashers import make_password

    user = UserModel.objects.create(
        email=user_data["email"],
        password_hash=make_password(user_data["password"]),
        is_active=True,
    )
    return user


@pytest.fixture
@pytest.mark.django_db
def jwt_token(create_user: Any, user_data: dict[str, str], api_client: APIClient) -> str:
    """
    Fixture to generate JWT token for authenticated requests.

    Args:
        create_user: Created user from fixture
        user_data: User credentials
        api_client: API client

    Returns:
        JWT access token
    """
    response = api_client.post(
        "/api/v1/token/", {"email": user_data["email"], "password": user_data["password"]}
    )

    if response.status_code == 200:
        return response.data["access"]

    # Fallback: generate token manually
    from rest_framework_simplejwt.tokens import RefreshToken

    refresh = RefreshToken()
    refresh["user_id"] = create_user.id
    refresh["email"] = create_user.email

    return str(refresh.access_token)


@pytest.fixture
@pytest.mark.django_db
def authenticated_client(
    api_client: APIClient, jwt_token: str
) -> APIClient:
    """
    Fixture for authenticated API client.

    Args:
        api_client: Base API client
        jwt_token: JWT access token

    Returns:
        APIClient with authentication header set
    """
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
    return api_client
