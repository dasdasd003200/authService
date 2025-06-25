# ===== MODIFICAR: config/strawberry_schema.py =====
import strawberry
from src.feature.users.presentation.graphql.resolvers.mutations.create import UserCreateResolver
from src.feature.users.presentation.graphql.resolvers.mutations.update import UserUpdateResolver
from src.feature.users.presentation.graphql.resolvers.mutations.delete import UserDeleteResolver
from src.feature.users.presentation.graphql.resolvers.queries.find import UserFindResolver
from src.feature.users.presentation.graphql.resolvers.queries.find_one import UserFindOneResolver


@strawberry.type
class Query(
    UserFindResolver,
    UserFindOneResolver,
):
    """Main GraphQL queries"""

    @strawberry.field
    def health(self) -> str:
        """Health check endpoint"""
        return "Auth Service is running!"


@strawberry.type
class Mutation(
    UserCreateResolver,
    UserUpdateResolver,
    UserDeleteResolver,
):
    """Main GraphQL mutations"""

    pass


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)

