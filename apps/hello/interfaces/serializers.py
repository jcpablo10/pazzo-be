"""
DRF Serializers for the Hello application.
Interfaces layer - API input/output.
"""
from __future__ import annotations

from typing import Any, Optional

from rest_framework import serializers


class HelloWorldSerializer(serializers.Serializer):
    """Serializer for Hello World response."""

    message = serializers.CharField(read_only=True)
    user = serializers.EmailField(read_only=True, required=False, allow_null=True)
    timestamp = serializers.DateTimeField(read_only=True, required=False)

    def to_representation(self, instance: Any) -> dict[str, Any]:
        """
        Convert HelloMessage entity to dictionary.

        Args:
            instance: HelloMessage entity

        Returns:
            Dictionary representation
        """
        from ..domain.entities import HelloMessage

        if isinstance(instance, HelloMessage):
            return {
                "message": instance.message,
                "user": instance.user_email,
                "timestamp": instance.timestamp.isoformat() if instance.timestamp else None,
            }

        return super().to_representation(instance)
