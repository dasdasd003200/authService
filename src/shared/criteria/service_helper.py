from typing import List, Dict, Any, Optional
from .input_converter import CriteriaInputConverter
from .prepare import PrepareFind, PrepareFindOne
from .base_criteria import Criteria, Filters, Orders, Filter, Order, FilterOperator, SortDirection
from uuid import UUID


class CriteriaServiceHelper:
    def __init__(self, feature_name: str, search_fields: List[str] = None, boolean_fields: List[str] = None, string_fields: List[str] = None, additional_field_mapping: Dict[str, str] = None):
        self.feature_name = feature_name
        self.search_fields = search_fields or []
        self.boolean_fields = boolean_fields or []
        self.string_fields = string_fields or []
        self.additional_field_mapping = additional_field_mapping or {}

    def build_find_prepare(self, input_obj) -> PrepareFind:
        # First try direct criteria (modern approach)
        if hasattr(input_obj, "criteria") and input_obj.criteria:
            criteria = CriteriaInputConverter.from_graphql_input(input_obj.criteria)
            return PrepareFind(criteria=criteria)

        # Fallback to legacy fields (backward compatibility)
        criteria = self._build_legacy_find_criteria(input_obj)
        return PrepareFind(criteria=criteria)

    def build_find_one_prepare(self, input_obj) -> PrepareFindOne:
        """
        Build PrepareFindOne from ANY feature's input
        Handles both direct criteria AND legacy fields
        """
        # First try direct criteria (modern approach)
        if hasattr(input_obj, "criteria") and input_obj.criteria:
            criteria = CriteriaInputConverter.from_graphql_input(input_obj.criteria)
            return PrepareFindOne(filters=criteria.filters)

        # Fallback to legacy fields (backward compatibility)
        criteria = self._build_legacy_find_one_criteria(input_obj)
        return PrepareFindOne(filters=criteria.filters)

    # ===== INLINE LEGACY BUILDER (sin dependencia externa) =====

    def _build_legacy_find_criteria(self, input_obj) -> Criteria:
        """Build find criteria from legacy input fields - inline implementation"""
        builder = Criteria.builder()
        filters = []

        # Extract common fields
        status = getattr(input_obj, "status", None)
        search_text = getattr(input_obj, "search_text", None)
        page = getattr(input_obj, "page", 1)
        page_size = getattr(input_obj, "page_size", 10)
        order_by = getattr(input_obj, "order_by", None)

        # ===== STATUS FILTER =====
        if status:
            filters.append(Filter(field="status", operator=FilterOperator.EQ, value=status))

        # ===== BOOLEAN FILTERS =====
        for field in self.boolean_fields:
            value = getattr(input_obj, field, None)
            if value is not None:
                filters.append(Filter(field=field, operator=FilterOperator.EQ, value=value))

        # ===== STRING FILTERS =====
        for field in self.string_fields:
            value = getattr(input_obj, field, None)
            if value:
                filters.append(Filter(field=field, operator=FilterOperator.EQ, value=value))

        # ===== TEXT SEARCH =====
        if search_text and self.search_fields:
            search_filters = []
            for field in self.search_fields:
                search_filters.append(Filter(field=field, operator=FilterOperator.ICONTAINS, value=search_text))

            # Add OR filter for search
            filters.append(Filter(field="", operator=FilterOperator.OR, value=None, nested_filters=search_filters))

        # Set filters
        if filters:
            builder.set_filters(Filters(filters))

        # ===== ORDERING =====
        orders = []
        if order_by:
            for order_field in order_by:
                if order_field.startswith("-"):
                    orders.append(Order(field=order_field[1:], direction=SortDirection.DESC))
                else:
                    orders.append(Order(field=order_field, direction=SortDirection.ASC))
        else:
            # Default order by created_at DESC
            orders.append(Order(field="created_at", direction=SortDirection.DESC))

        builder.set_orders(Orders(orders))

        # ===== PAGINATION =====
        offset = (page - 1) * page_size
        builder.set_limit(page_size)
        builder.set_offset(offset)

        return builder.build()

    def _build_legacy_find_one_criteria(self, input_obj) -> Criteria:
        """Build findOne criteria from legacy input fields - inline implementation"""
        filters = []

        # ===== ID FILTER (most common) =====
        entity_id = getattr(input_obj, f"{self.feature_name}_id", None)
        if not entity_id:
            entity_id = getattr(input_obj, "id", None)

        if entity_id:
            filters.append(Filter(field="id", operator=FilterOperator.EQ, value=UUID(entity_id)))

        # ===== STRING FILTERS =====
        for field in self.string_fields:
            value = getattr(input_obj, field, None)
            if value:
                filters.append(Filter(field=field, operator=FilterOperator.EQ, value=value))

        return Criteria(filters=Filters(filters))

