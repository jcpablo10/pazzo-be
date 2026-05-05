"""
URL routing for the Users application.
"""
from __future__ import annotations

from django.urls import path
from rest_framework.routers import DefaultRouter

from .viewsets import UserViewSet

app_name = "users"

router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")

urlpatterns = router.urls
