from src.core.infrastructure.web.strawberry.responses import CreateResponse, UpdateResponse, DeleteResponse, FindResponse, FindOneResponse
from ..schemes.user import UserGraphQLType

# Type aliases para User - Estos son los tipos que usa el GraphQL schema
UserCreateResponse = CreateResponse[UserGraphQLType]
UserUpdateResponse = UpdateResponse[UserGraphQLType]
UserDeleteResponse = DeleteResponse
UserFindResponse = FindResponse[UserGraphQLType]
UserFindOneResponse = FindOneResponse[UserGraphQLType]

