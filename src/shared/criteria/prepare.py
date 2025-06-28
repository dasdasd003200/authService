from typing import TypeVar, Generic
from dataclasses import dataclass
from .base_criteria import Criteria, Filters

T = TypeVar("T")


@dataclass
class PrepareFind(Generic[T]):
    """Prepare class for find operations - generic for any entity"""

    criteria: Criteria

    def __init__(self, criteria: Criteria):
        self.criteria = criteria


@dataclass
class PrepareFindOne(Generic[T]):
    """Prepare class for findOne operations - generic for any entity"""

    criteria: Criteria

    def __init__(self, filters: Filters):
        self.criteria = Criteria(filters=filters)
