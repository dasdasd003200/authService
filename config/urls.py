# config/urls.py
"""
URL configuration for authservice project with Strawberry GraphQL.
"""

from django.contrib import admin
from django.urls import path
from strawberry.django.views import GraphQLView

from .strawberry_schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", GraphQLView.as_view(schema=schema)),
]

