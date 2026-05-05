"""
DRF Serializers for the Users application.
Interfaces layer - API input/output.
"""
from __future__ import annotations

from typing import Any

from rest_framework import serializers

from ..application.dtos import UserInputDTO, UserOutputDTO
from ..application.services import RegisterUserUseCase
from ..infrastructure.repositories import DjangoUserRepository


class UserSerializer(serializers.Serializer):
    """Serializer for User output."""

    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, required=False)


class UserRegistrationSerializer(serializers.Serializer):
    """Serializer for user registration."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        min_length=8, max_length=128, write_only=True, required=True
    )

    def create(self, validated_data: dict[str, Any]) -> UserOutputDTO:
        """
        Create a new user using the RegisterUserUseCase.

        Args:
            validated_data: Validated input data

        Returns:
            UserOutputDTO instance

        Raises:
            ValidationError: If user already exists
        """
        # Create DTO from validated data
        input_dto = UserInputDTO(
            email=validated_data["email"], password=validated_data["password"]
        )

        # Execute use case
        repository = DjangoUserRepository()
        use_case = RegisterUserUseCase(repository)

        try:
            user_dto = use_case.execute(input_dto)
            return user_dto
        except Exception as e:
            raise serializers.ValidationError(str(e))


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
