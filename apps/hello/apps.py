"""
Django app configuration for Hello application.
"""
from __future__ import annotations

from django.apps import AppConfig


class HelloConfig(AppConfig):
    """Configuration for the Hello app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.hello"
    verbose_name = "Hello"

    def ready(self) -> None:
        """Initialize app when Django starts."""
        pass
