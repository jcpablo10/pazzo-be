"""
DRF ViewSets for the Hello application.
Interfaces layer - API endpoints.
"""
from __future__ import annotations

from typing import Any

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..application.services import GetHelloMessageUseCase
from .serializers import HelloWorldSerializer


class HelloWorldViewSet(viewsets.ViewSet):
    """
    ViewSet for Hello World endpoint.
    Requires JWT authentication.
    """

    permission_classes = [IsAuthenticated]

    def list(self, request: Request) -> Response:
        """
        Return a hello world message.

        GET /api/v1/hello/

        Requires: JWT Authentication header
        Returns: {
            "message": "Hello World from Pazzo!",
            "user": "user@example.com",
            "timestamp": "2024-01-01T12:00:00"
        }
        """
        # Get authenticated user's email
        user_email: str = ""
        if hasattr(request.user, "email"):
            user_email = request.user.email
        elif hasattr(request, "auth") and request.auth:
            # For JWT tokens, extract email from token payload
            from rest_framework_simplejwt.tokens import AccessToken

            try:
                # Get user from database using token's user_id
                from apps.users.infrastructure.models import UserModel

                token = AccessToken(request.auth)
                user_id = token.get("user_id")
                if user_id:
                    try:
                        user = UserModel.objects.get(id=user_id)
                        user_email = user.email
                    except UserModel.DoesNotExist:
                        pass
            except Exception:
                pass

        # Execute use case
        use_case = GetHelloMessageUseCase()
        hello_message = use_case.execute(user_email=user_email if user_email else None)

        # Serialize and return
        serializer = HelloWorldSerializer(hello_message)
        return Response(serializer.data, status=status.HTTP_200_OK)
