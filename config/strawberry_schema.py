import strawberry

from src.feature.users.infrastructure.graphql.user_resolvers import UserQueries, UserMutations


@strawberry.type
class Query(UserQueries):
    @strawberry.field
    def health(self) -> str:
        return "Auth Service is running!"


@strawberry.type
class Mutation(UserMutations):
    pass


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)
