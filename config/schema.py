# config/schema.py
import graphene
from src.feature.users.infrastructure.web.graphql.mutations import UserMutations
from src.feature.users.infrastructure.web.graphql.queries import UserQueries


class Query(UserQueries, graphene.ObjectType):
    """Main GraphQL queries"""

    health = graphene.String()

    def resolve_health(self, _):
        return "Auth Service is running!"


class Mutation(UserMutations, graphene.ObjectType):
    """Main GraphQL mutations"""

    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
