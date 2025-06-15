import graphene


class Query(graphene.ObjectType):
    health = graphene.String()

    def resolve_health(self, info):
        return "Auth Service is running!"


schema = graphene.Schema(query=Query)

