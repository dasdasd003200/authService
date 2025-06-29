# config/strawberry_schema.py
import strawberry

from src.feature.users.infrastructure.graphql.user_resolvers import UserQueries, UserMutations
from src.feature.sessions.infrastructure.graphql.auth_resolvers import AuthQueries, AuthMutations


@strawberry.type
class Query(UserQueries, AuthQueries):
    @strawberry.field
    def health(self) -> str:
        return "Auth Service is running! 🚀"


@strawberry.type
class Mutation(UserMutations, AuthMutations):
    pass


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)

