from datetime import datetime
from typing import Optional
from django.db.models import QuerySet
from .base_criteria import BaseCriteria


class DateRangeCriteria(BaseCriteria):
    def __init__(
        self,
        field_name: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ):
        self.field_name = field_name
        self.start_date = start_date
        self.end_date = end_date

    def apply(self, queryset: QuerySet) -> QuerySet:
        filters = {}

        if self.start_date:
            filters[f"{self.field_name}__gte"] = self.start_date

        if self.end_date:
            filters[f"{self.field_name}__lte"] = self.end_date

        return queryset.filter(**filters) if filters else queryset

    def to_dict(self) -> dict:
        return {
            "type": "date_range",
            "field": self.field_name,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
        }
