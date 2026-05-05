"""
Django app configuration for Users application.
"""
from __future__ import annotations

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Configuration for the Users app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"
    verbose_name = "Users"

    def ready(self) -> None:
        """Initialize app when Django starts."""
        pass
