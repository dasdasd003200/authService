# config/strawberry_schema.py
"""
Main Strawberry GraphQL schema.
"""

import strawberry

from src.feature.users.infrastructure.web.strawberry.mutations import UserMutations
from src.feature.users.infrastructure.web.strawberry.queries import UserQueries


@strawberry.type
class Query(UserQueries):
    """Main GraphQL queries"""

    @strawberry.field
    def health(self) -> str:
        """Health check endpoint"""
        return "Auth Service is running!"


@strawberry.type
class Mutation(UserMutations):
    """Main GraphQL mutations"""

    pass


# Create the schema
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)
