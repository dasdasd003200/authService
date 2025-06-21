# src/core/domain/repositories/criteria/text_search_criteria.py
from typing import List
from django.db.models import QuerySet, Q
from .base_criteria import BaseCriteria


class TextSearchCriteria(BaseCriteria):
    """Criteria for text search across multiple fields"""

    def __init__(self, search_term: str, fields: List[str]):
        self.search_term = search_term.strip()
        self.fields = fields

    def apply(self, queryset: QuerySet) -> QuerySet:
        if not self.search_term:
            return queryset

        # Create Q objects for each field
        query = Q()
        for field in self.fields:
            query |= Q(**{f"{field}__icontains": self.search_term})

        return queryset.filter(query)

    def to_dict(self) -> dict:
        return {
            "type": "text_search",
            "search_term": self.search_term,
            "fields": self.fields,
        }
