# src/shared/criteria/__init__.py
"""
Criteria system for repository filtering and querying
"""

# Base classes
from .base_criteria import BaseCriteria, CriteriaBuilder

# Factory
from .factory import CriteriaFactory

# All implementations (optional - for convenience)
from .implementations import *

__all__ = [
    # Base
    "BaseCriteria",
    "CriteriaBuilder",
    # Factory
    "CriteriaFactory",
]
