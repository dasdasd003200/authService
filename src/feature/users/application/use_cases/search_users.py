from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.domain.entities.user import User
from src.shared.criteria.factory import CriteriaFactory
from src.shared.criteria.base_criteria import CriteriaBuilder


@dataclass
class SearchUsersQuery:
    status: Optional[str] = None
    email_verified: Optional[bool] = None
    search_text: Optional[str] = None
    page: int = 1
    page_size: int = 10


@dataclass
class UserSearchResult:
    user_id: str
    email: str
    first_name: str
    last_name: str
    full_name: str
    status: str
    email_verified: bool
    created_at: datetime


class SearchUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, query: SearchUsersQuery) -> List[UserSearchResult]:
        criteria_builder = CriteriaBuilder()

        # Filtros de users
        if query.status:
            criteria_builder.add(CriteriaFactory.status(query.status))

        if query.email_verified is not None:
            criteria_builder.add(CriteriaFactory.boolean_field("email_verified", query.email_verified))

        if query.search_text:
            criteria_builder.add(CriteriaFactory.text_search(query.search_text, ["first_name", "last_name", "email"]))

        offset = (query.page - 1) * query.page_size
        criteria_builder.add(CriteriaFactory.paginate(query.page_size, offset))

        users = await self.user_repository.find_by_criteria(criteria_builder.build())
        return self._convert_entities_to_results(users)

    def _convert_entities_to_results(self, users: List[User]) -> List[UserSearchResult]:
        """Convert domain entities to result objects"""
        return [
            UserSearchResult(
                user_id=str(user.id),
                email=str(user.email),
                first_name=user.first_name,
                last_name=user.last_name,
                full_name=user.full_name,
                status=user.status.value,
                email_verified=user.email_verified,
                created_at=user.created_at,
            )
            for user in users
        ]

