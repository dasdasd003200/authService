from django.db.models import QuerySet
from ..base_criteria import BaseCriteria


class PaginationCriteria(BaseCriteria):
    """Criteria for pagination"""

    def __init__(self, limit: int, offset: int):
        self.limit = limit
        self.offset = offset

    def apply(self, queryset: QuerySet) -> QuerySet:
        return queryset[self.offset : self.offset + self.limit]

    def to_dict(self) -> dict:
        return {
            "type": "pagination",
            "limit": self.limit,
            "offset": self.offset,
        }
