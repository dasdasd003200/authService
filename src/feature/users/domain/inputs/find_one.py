import strawberry
from src.shared.criteria.graphql_inputs import CriteriaInput


@strawberry.input
class UserFindOneInput:
    criteria: CriteriaInput = strawberry.field(description="Universal criteria - must specify filters to find a specific user")

