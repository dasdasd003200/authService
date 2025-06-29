from src.core.infrastructure.web.strawberry.responses import CreateResponse, UpdateResponse, DeleteResponse, FindResponse, FindOneResponse
from ..schemes.user import UserGraphQLType

UserCreateResponse = CreateResponse[UserGraphQLType]
UserUpdateResponse = UpdateResponse[UserGraphQLType]
UserDeleteResponse = DeleteResponse
UserFindResponse = FindResponse[UserGraphQLType]
UserFindOneResponse = FindOneResponse[UserGraphQLType]
