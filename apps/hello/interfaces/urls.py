"""
URL routing for the Hello application.
"""
from __future__ import annotations

from rest_framework.routers import DefaultRouter

from .viewsets import HelloWorldViewSet

app_name = "hello"

router = DefaultRouter()
router.register(r"", HelloWorldViewSet, basename="hello")

urlpatterns = router.urls
