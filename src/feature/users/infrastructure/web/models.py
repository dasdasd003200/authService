# src/feature/users/infrastructure/web/models.py
"""
Models for the users web app.
This file imports the actual models from the database layer to make them
available to Django's app system.
"""

# Import the models from the database layer
from src.feature.users.infrastructure.database.models import UserModel

# Make the model available at the app level
__all__ = ["UserModel"]
