"""
Application services (Use Cases) for the Users application.
Contains business logic orchestration.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.hashers import make_password

from ..domain.entities import User
from ..domain.exceptions import (
    InactiveUserException,
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from .dtos import UserInputDTO, UserOutputDTO
from .ports import UserRepository

if TYPE_CHECKING:
    from typing import Optional


class RegisterUserUseCase:
    """Use case for registering a new user."""

    def __init__(self, user_repository: UserRepository) -> None:
        """
        Initialize the use case.

        Args:
            user_repository: Repository for user data access
        """
        self.user_repository = user_repository

    def execute(self, input_dto: UserInputDTO) -> UserOutputDTO:
        """
        Execute the user registration use case.

        Args:
            input_dto: User input data

        Returns:
            UserOutputDTO with created user data

        Raises:
            UserAlreadyExistsException: If user with email already exists
        """
        # Check if user already exists
        if self.user_repository.exists_by_email(input_dto.email):
            raise UserAlreadyExistsException(input_dto.email)

        # Create domain entity
        user = User(
            email=input_dto.email,
            password_hash=make_password(input_dto.password),
            is_active=True,
        )

        # Save through repository
        saved_user = self.user_repository.save(user)

        # Return DTO
        return UserOutputDTO.from_entity(saved_user)


class GetUserByEmailUseCase:
    """Use case for retrieving a user by email."""

    def __init__(self, user_repository: UserRepository) -> None:
        """
        Initialize the use case.

        Args:
            user_repository: Repository for user data access
        """
        self.user_repository = user_repository

    def execute(self, email: str) -> UserOutputDTO:
        """
        Execute the get user by email use case.

        Args:
            email: User's email address

        Returns:
            UserOutputDTO with user data

        Raises:
            UserNotFoundException: If user is not found
        """
        user = self.user_repository.find_by_email(email)

        if user is None:
            raise UserNotFoundException(email)

        return UserOutputDTO.from_entity(user)


class AuthenticateUserUseCase:
    """Use case for authenticating a user."""

    def __init__(self, user_repository: UserRepository) -> None:
        """
        Initialize the use case.

        Args:
            user_repository: Repository for user data access
        """
        self.user_repository = user_repository

    def execute(self, email: str, password: str) -> UserOutputDTO:
        """
        Authenticate a user with email and password.

        Args:
            email: User's email
            password: User's password

        Returns:
            UserOutputDTO if authentication succeeds

        Raises:
            InvalidCredentialsException: If credentials are invalid
        """
        user = self.user_repository.find_by_email(email)

        if user is None or not user.verify_password(password):
            raise InvalidCredentialsException()

        if not user.is_active:
            raise InactiveUserException()

        return UserOutputDTO.from_entity(user)
