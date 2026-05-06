"""
DRF ViewSets for the Users application.
Interfaces layer - API endpoints.
"""
from __future__ import annotations

from typing import Any

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from ..application.services import (
    AuthenticateUserUseCase,
    GetUserByEmailUseCase,
)
from ..domain.exceptions import (
    InactiveUserException,
    InvalidCredentialsException,
    UserNotFoundException,
)
from ..infrastructure.repositories import DjangoUserRepository
from .serializers import UserLoginSerializer, UserRegistrationSerializer, UserSerializer


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

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request: Request) -> Response:
        """
        Authenticate a user and return JWT tokens.

        POST /api/v1/users/login/
        {
            "email": "user@example.com",
            "password": "securepassword"
        }
        """
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        # Execute authentication use case
        repository = DjangoUserRepository()
        use_case = AuthenticateUserUseCase(repository)

        try:
            user_dto = use_case.execute(email, password)

            # Get the Django User model for token generation
            django_user = repository.find_django_user_by_email(email)
            if not django_user:
                return Response(
                    {"detail": "Authentication failed"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(django_user)

            return Response(
                {
                    "user": UserSerializer(user_dto).data,
                    "tokens": {
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                    },
                },
                status=status.HTTP_200_OK,
            )

        except InvalidCredentialsException:
            return Response(
                {"detail": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except InactiveUserException:
            return Response(
                {"detail": "User account is inactive"},
                status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            return Response(
                {"detail": "Authentication failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
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

        # Get user email from authenticated Django user
        user_email = request.user.email

        # Fetch user from repository
        repository = DjangoUserRepository()
        use_case = GetUserByEmailUseCase(repository)

        try:
            user_dto = use_case.execute(user_email)
            return Response(UserSerializer(user_dto).data, status=status.HTTP_200_OK)

        except UserNotFoundException:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            return Response(
                {"detail": "Failed to retrieve user"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def logout(self, request: Request) -> Response:
        """
        Logout user by blacklisting the refresh token.

        POST /api/v1/users/logout/
        {
            "refresh": "refresh_token_here"
        }
        """
        try:
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response(
                    {"detail": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"detail": "Successfully logged out"}, status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                {"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )
