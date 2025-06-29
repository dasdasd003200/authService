# src/feature/users/domain/inputs/find_one.py
import strawberry
from typing import Optional
from src.shared.criteria.graphql_inputs import CriteriaInput


@strawberry.input
class UserFindOneInput:
    criteria: CriteriaInput = strawberry.field(description="Universal criteria - must specify filters to find a specific user")

