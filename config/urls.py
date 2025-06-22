# config/urls.py - VOLVER A ASYNC
"""
URL configuration for authservice project with Strawberry GraphQL.
"""

from django.contrib import admin
from django.urls import path
from strawberry.django.views import AsyncGraphQLView  # ✅ VOLVER A ASYNC

from .strawberry_schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    # ✅ VOLVER A AsyncGraphQLView
    path("graphql/", AsyncGraphQLView.as_view(schema=schema)),
]
