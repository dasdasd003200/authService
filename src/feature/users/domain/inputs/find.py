import strawberry
from typing import Optional
from src.shared.criteria.graphql_inputs import CriteriaInput


@strawberry.input
class UserFindInput:
    criteria: Optional[CriteriaInput] = strawberry.field(default=None, description="Universal criteria - filter, sort, paginate any field")
