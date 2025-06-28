# src/shared/criteria/base_criteria.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Generic
from django.db.models import QuerySet
from enum import Enum
from dataclasses import dataclass


class FilterOperator(Enum):
    """General filter operators for any field type"""

    EQ = "eq"  # Equal
    NE = "ne"  # Not Equal
    GT = "gt"  # Greater Than
    GTE = "gte"  # Greater Than or Equal
    LT = "lt"  # Less Than
    LTE = "lte"  # Less Than or Equal
    IN = "in"  # In list
    NIN = "nin"  # Not In list
    CONTAINS = "contains"  # Contains (for strings)
    ICONTAINS = "icontains"  # Case-insensitive contains
    STARTSWITH = "startswith"  # Starts with
    ENDSWITH = "endswith"  # Ends with
    ISNULL = "isnull"  # Is null
    REGEX = "regex"  # Regex match
    AND = "and"  # Logical AND
    OR = "or"  # Logical OR


class SortDirection(Enum):
    """Sort directions"""

    ASC = "asc"
    DESC = "desc"


@dataclass
class Filter:
    """Individual filter - completely generic"""

    field: str
    operator: FilterOperator
    value: Any
    nested_filters: Optional[List["Filter"]] = None

    def to_django_lookup(self) -> Dict[str, Any]:
        """Convert to Django ORM lookup"""
        if self.operator == FilterOperator.AND and self.nested_filters:
            return {"__and": [f.to_django_lookup() for f in self.nested_filters]}
        elif self.operator == FilterOperator.OR and self.nested_filters:
            return {"__or": [f.to_django_lookup() for f in self.nested_filters]}

        # Map operators to Django field lookups
        operator_map = {
            FilterOperator.EQ: "",
            FilterOperator.GT: "__gt",
            FilterOperator.GTE: "__gte",
            FilterOperator.LT: "__lt",
            FilterOperator.LTE: "__lte",
            FilterOperator.IN: "__in",
            FilterOperator.CONTAINS: "__contains",
            FilterOperator.ICONTAINS: "__icontains",
            FilterOperator.STARTSWITH: "__startswith",
            FilterOperator.ENDSWITH: "__endswith",
            FilterOperator.ISNULL: "__isnull",
            FilterOperator.REGEX: "__regex",
        }

        # Handle special cases for operators not directly supported by Django
        if self.operator == FilterOperator.NE:
            # For "not equal", we'll handle this in the converter using exclude()
            lookup_key = self.field if self.field else "pk"
            return {f"_exclude_{lookup_key}": self.value}
        elif self.operator == FilterOperator.NIN:
            # For "not in", we'll handle this in the converter using exclude()
            lookup_key = f"{self.field}__in" if self.field else "pk__in"
            return {f"_exclude_{lookup_key}": self.value}

        lookup_suffix = operator_map.get(self.operator, "")
        lookup_key = f"{self.field}{lookup_suffix}"
        return {lookup_key: self.value}


@dataclass
class Order:
    """Individual order - completely generic"""

    field: str
    direction: SortDirection = SortDirection.ASC

    def to_django_order(self) -> str:
        """Convert to Django order_by format"""
        if self.direction == SortDirection.DESC:
            return f"-{self.field}"
        return self.field


@dataclass
class Projection:
    """Field projection - completely generic"""

    fields: List[str]

    def to_django_values(self) -> List[str]:
        """Convert to Django .values() format"""
        return self.fields


class Filters:
    """Collection of filters - generic for any entity"""

    def __init__(self, filters: List[Filter]):
        self.filters = filters

    @classmethod
    def none(cls) -> "Filters":
        """Create empty filters"""
        return cls([])

    @classmethod
    def from_input(cls, filter_inputs: List[Dict[str, Any]]) -> "Filters":
        """Create from input data - generic"""
        filters = []
        for input_data in filter_inputs:
            filter_obj = Filter(field=input_data.get("field", ""), operator=FilterOperator(input_data.get("operator", "eq")), value=input_data.get("value"), nested_filters=None)
            filters.append(filter_obj)
        return cls(filters)


class Orders:
    """Collection of orders - generic for any entity"""

    def __init__(self, orders: List[Order]):
        self.orders = orders

    @classmethod
    def none(cls) -> "Orders":
        """Create empty orders"""
        return cls([])

    @classmethod
    def from_input(cls, order_inputs: List[Dict[str, Any]]) -> "Orders":
        """Create from input data - generic"""
        orders = []
        for input_data in order_inputs:
            order_obj = Order(field=input_data.get("field", ""), direction=SortDirection(input_data.get("direction", "asc")))
            orders.append(order_obj)
        return cls(orders)

    def to_django_order_by(self) -> List[str]:
        """Convert to Django order_by format"""
        return [order.to_django_order() for order in self.orders]


@dataclass
class CriteriaOptions:
    """Additional options for criteria - generic"""

    explain: bool = False
    max_time_ms: Optional[int] = None
    comment: Optional[str] = None
    batch_size: Optional[int] = None


class Criteria:
    """Main criteria class - completely generic for any entity"""

    def __init__(self, filters: Filters = None, orders: Orders = None, limit: Optional[int] = None, offset: Optional[int] = None, projection: Optional[Projection] = None, options: Optional[CriteriaOptions] = None):
        self.filters = filters or Filters.none()
        self.orders = orders or Orders.none()
        self.limit = limit
        self.offset = offset
        self.projection = projection
        self.options = options or CriteriaOptions()

    def has_filters(self) -> bool:
        return len(self.filters.filters) > 0

    def has_orders(self) -> bool:
        return len(self.orders.orders) > 0

    def has_projection(self) -> bool:
        return self.projection is not None and len(self.projection.fields) > 0

    def has_pagination(self) -> bool:
        return self.limit is not None or self.offset is not None

    @classmethod
    def builder(cls) -> "CriteriaBuilder":
        """Create builder instance"""
        return CriteriaBuilder()


class CriteriaBuilder:
    """Builder for Criteria - generic for any use case"""

    def __init__(self):
        self._filters: Filters = Filters.none()
        self._orders: Orders = Orders.none()
        self._limit: Optional[int] = None
        self._offset: Optional[int] = None
        self._projection: Optional[Projection] = None
        self._options: CriteriaOptions = CriteriaOptions()

    def set_filters(self, filters: Filters) -> "CriteriaBuilder":
        self._filters = filters
        return self

    def set_orders(self, orders: Orders) -> "CriteriaBuilder":
        self._orders = orders
        return self

    def set_limit(self, limit: int) -> "CriteriaBuilder":
        self._limit = limit
        return self

    def set_offset(self, offset: int) -> "CriteriaBuilder":
        self._offset = offset
        return self

    def set_projection(self, projection: Projection) -> "CriteriaBuilder":
        self._projection = projection
        return self

    def set_explain(self, explain: bool) -> "CriteriaBuilder":
        self._options.explain = explain
        return self

    def set_comment(self, comment: str) -> "CriteriaBuilder":
        self._options.comment = comment
        return self

    def build(self) -> Criteria:
        return Criteria(filters=self._filters, orders=self._orders, limit=self._limit, offset=self._offset, projection=self._projection, options=self._options)

