# config/schema.py
import graphene
from src.feature.users.infrastructure.web.graphql.mutations import UserMutations


class Query(graphene.ObjectType):
    health = graphene.String()

    def resolve_health(self, _):
        return "Auth Service is running!"


class Mutation(UserMutations, graphene.ObjectType):
    """Mutations principales del servicio"""

    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

