"""
Unit tests for Hello domain entities.
These tests have no Django dependencies.
"""
from __future__ import annotations

import pytest
from datetime import datetime

from apps.hello.domain.entities import HelloMessage


@pytest.mark.unit
class TestHelloMessage:
    """Test suite for HelloMessage entity."""

    def test_create_hello_message_without_user(self) -> None:
        """Test creating a hello message without user email."""
        message = HelloMessage(message="Hello World from Pazzo!")

        assert message.message == "Hello World from Pazzo!"
        assert message.user_email is None
        assert message.timestamp is not None
        assert isinstance(message.timestamp, datetime)

    def test_create_hello_message_with_user(self) -> None:
        """Test creating a hello message with user email."""
        message = HelloMessage(
            message="Hello World from Pazzo!", user_email="test@example.com"
        )

        assert message.message == "Hello World from Pazzo!"
        assert message.user_email == "test@example.com"
        assert message.timestamp is not None

    def test_get_full_message_without_user(self) -> None:
        """Test getting full message without user."""
        message = HelloMessage(message="Hello World from Pazzo!")

        full_message = message.get_full_message()

        assert full_message == "Hello World from Pazzo!"

    def test_get_full_message_with_user(self) -> None:
        """Test getting full message with user."""
        message = HelloMessage(
            message="Hello World from Pazzo!", user_email="test@example.com"
        )

        full_message = message.get_full_message()

        assert full_message == "Hello World from Pazzo! Welcome, test@example.com!"

    def test_string_representation(self) -> None:
        """Test string representation of HelloMessage."""
        message = HelloMessage(
            message="Hello World from Pazzo!", user_email="test@example.com"
        )

        assert str(message) == "Hello World from Pazzo! Welcome, test@example.com!"
