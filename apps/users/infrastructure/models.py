"""
Django ORM models for the Users application.
Infrastructure layer - persistence.
"""
from __future__ import annotations

from django.contrib.auth.hashers import make_password
from django.db import models


class UserModel(models.Model):
    """
    Django ORM model for User.
    This is the infrastructure/persistence representation.
    """

    email = models.EmailField(unique=True, max_length=255, db_index=True)
    password_hash = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.email

    def set_password(self, raw_password: str) -> None:
        """Set the user's password (hashed)."""
        self.password_hash = make_password(raw_password)
