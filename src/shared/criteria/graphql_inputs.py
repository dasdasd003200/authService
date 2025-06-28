import strawberry
from typing import List, Optional
from enum import Enum


@strawberry.enum
class FilterOperatorInput(Enum):
    EQ = "eq"
    NE = "ne"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    NIN = "nin"
    CONTAINS = "contains"
    ICONTAINS = "icontains"
    STARTSWITH = "startswith"
    ENDSWITH = "endswith"
    ISNULL = "isnull"
    REGEX = "regex"
    AND = "and"
    OR = "or"


@strawberry.enum
class SortDirectionInput(Enum):
    ASC = "asc"
    DESC = "desc"


@strawberry.input
class FilterInput:
    field: Optional[str] = strawberry.field(default=None, description="Field to filter on")
    operator: FilterOperatorInput = strawberry.field(description="Filter operator")
    value: Optional[str] = strawberry.field(default=None, description="Filter value")
    nested_filters: Optional[List["FilterInput"]] = strawberry.field(default=None, description="Nested filters for AND/OR operations")


@strawberry.input
class OrderInput:
    field: str = strawberry.field(description="Field to order by")
    direction: SortDirectionInput = strawberry.field(default=SortDirectionInput.ASC, description="Sort direction")


@strawberry.input
class ProjectionInput:
    fields: List[str] = strawberry.field(description="Fields to include in response")


@strawberry.input
class CriteriaOptionsInput:
    explain: bool = strawberry.field(default=False, description="Explain query execution")
    comment: Optional[str] = strawberry.field(default=None, description="Query comment for debugging")
    batch_size: Optional[int] = strawberry.field(default=None, description="Batch size for query")


@strawberry.input
class CriteriaInput:
    filters: Optional[List[FilterInput]] = strawberry.field(default=None, description="Query filters")
    orders: Optional[List[OrderInput]] = strawberry.field(default=None, description="Query ordering")
    limit: Optional[int] = strawberry.field(default=None, description="Limit number of results")
    offset: Optional[int] = strawberry.field(default=None, description="Offset for pagination")
    projection: Optional[ProjectionInput] = strawberry.field(default=None, description="Field projection")
    options: Optional[CriteriaOptionsInput] = strawberry.field(default=None, description="Additional query options")
