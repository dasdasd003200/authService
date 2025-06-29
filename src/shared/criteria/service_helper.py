# src/shared/criteria/service_helper.py
from typing import List, Dict, Any, Optional
from .input_converter import CriteriaInputConverter
from .prepare import PrepareFind, PrepareFindOne
from .base_criteria import Criteria, Filters, Orders, Filter, Order, FilterOperator, SortDirection
from src.core.exceptions.base_exceptions import ValidationException


class CriteriaServiceHelper:
    def __init__(self, feature_name: str, search_fields: List[str] = None, boolean_fields: List[str] = None, string_fields: List[str] = None, additional_field_mapping: Dict[str, str] = None):
        self.feature_name = feature_name
        self.search_fields = search_fields or []
        self.boolean_fields = boolean_fields or []
        self.string_fields = string_fields or []
        self.additional_field_mapping = additional_field_mapping or {}

    def build_find_prepare(self, input_obj) -> PrepareFind:
        if not hasattr(input_obj, "criteria") or not input_obj.criteria:
            # Provide default criteria with sensible defaults
            criteria = self._build_default_find_criteria()
        else:
            criteria = CriteriaInputConverter.from_graphql_input(input_obj.criteria)

        return PrepareFind(criteria=criteria)

    def build_find_one_prepare(self, input_obj) -> PrepareFindOne:
        if not hasattr(input_obj, "criteria") or not input_obj.criteria:
            raise ValidationException("Criteria is required for find operations. Please specify filters to search for a specific record.", error_code="CRITERIA_REQUIRED")

        criteria = CriteriaInputConverter.from_graphql_input(input_obj.criteria)
        return PrepareFindOne(filters=criteria.filters)

    def _build_default_find_criteria(self) -> Criteria:
        builder = Criteria.builder()

        # Default ordering by created_at DESC
        orders = [Order(field="created_at", direction=SortDirection.DESC)]
        builder.set_orders(Orders(orders))

        # Default pagination (first 10 records)
        builder.set_limit(10)
        builder.set_offset(0)

        return builder.build()
