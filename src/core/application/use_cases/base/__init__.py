# src/core/application/use_cases/base/__init__.py
"""
Base CRUD use cases - Modular structure
"""

# Commands and Queries
from .commands import (
    GetEntityByIdQuery,
    DeleteEntityCommand,
)

# Use Cases
from .get_entity import GetEntityByIdUseCase
from .delete_entity import DeleteEntityUseCase

# Main exports
__all__ = [
    # Commands/Queries
    "GetEntityByIdQuery",
    "DeleteEntityCommand",
    # Use Cases
    "GetEntityByIdUseCase",
    "DeleteEntityUseCase",
]
