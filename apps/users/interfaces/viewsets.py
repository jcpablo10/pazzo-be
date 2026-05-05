"""
DRF ViewSets for the Users application.
Interfaces layer - API endpoints.
"""
from __future__ import annotations

from typing import Any

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import UserRegistrationSerializer, UserSerializer


class UserViewSet(viewsets.ViewSet):
    """
    ViewSet for User operations.
    Handles HTTP requests and delegates to use cases.
    """

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def register(self, request: Request) -> Response:
        """
        Register a new user.

        POST /api/v1/users/register/
        {
            "email": "user@example.com",
            "password": "securepassword"
        }
        """
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user_dto = serializer.save()

            # Serialize the output
            output_serializer = UserSerializer(user_dto)

            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], permission_classes=[])
    def me(self, request: Request) -> Response:
        """
        Get current authenticated user.

        GET /api/v1/users/me/
        """
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # For now, return basic user info
        # In a real scenario, you'd fetch from repository
        data: dict[str, Any] = {
            "email": getattr(request.user, "email", ""),
            "is_active": getattr(request.user, "is_active", False),
        }

        return Response(data, status=status.HTTP_200_OK)
