from typing import List, Any, Optional
from datetime import datetime
from .implementations.text_search_criteria import TextSearchCriteria
from .implementations.status_criteria import StatusCriteria
from .implementations.boolean_criteria import BooleanCriteria
from .implementations.ordering_criteria import OrderingCriteria
from .implementations.in_criteria import InCriteria
from .implementations.range_criteria import RangeCriteria
from .implementations.date_range_criteria import DateRangeCriteria
from .implementations.pagination_criteria import PaginationCriteria


class CriteriaFactory:
    @staticmethod
    def text_search(search_term: str, fields: List[str]) -> TextSearchCriteria:
        return TextSearchCriteria(search_term, fields)

    @staticmethod
    def status(status: str, field_name: str = "status") -> StatusCriteria:
        return StatusCriteria(status, field_name)

    @staticmethod
    def boolean_field(field_name: str, value: bool) -> BooleanCriteria:
        return BooleanCriteria(field_name, value)

    @staticmethod
    def order_by(fields: List[str]) -> OrderingCriteria:
        return OrderingCriteria(fields)

    @staticmethod
    def field_in(field_name: str, values: List[Any]) -> InCriteria:
        return InCriteria(field_name, values)

    @staticmethod
    def number_range(
        field_name: str,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
    ) -> RangeCriteria:
        return RangeCriteria(field_name, min_value, max_value)

    @staticmethod
    def date_range(
        field_name: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> DateRangeCriteria:
        return DateRangeCriteria(field_name, start_date, end_date)

    @staticmethod
    def paginate(limit: int, offset: int) -> PaginationCriteria:
        return PaginationCriteria(limit, offset)
