"""
Main URL configuration for Pazzo project.
"""
from __future__ import annotations

from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # JWT Authentication
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # App URLs
    path("api/v1/users/", include("apps.users.interfaces.urls")),
    path("api/v1/hello/", include("apps.hello.interfaces.urls")),
]
