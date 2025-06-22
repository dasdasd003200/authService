# config/urls.py - CORREGIDO para async
"""
URL configuration for authservice project with Strawberry GraphQL.
"""

from django.contrib import admin
from django.urls import path
from strawberry.django.views import AsyncGraphQLView  # CAMBIADO: AsyncGraphQLView

from .strawberry_schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    # CORREGIDO: Usar AsyncGraphQLView en lugar de GraphQLView
    path("graphql/", AsyncGraphQLView.as_view(schema=schema)),
]

