# src/shared/criteria/converter.py
from django.db.models import QuerySet, Q
from functools import reduce
import operator
from .base_criteria import Criteria, Filters, FilterOperator, Filter


class CriteriaConverter:
    """Converts Criteria to Django QuerySet operations - generic for any model"""

    @staticmethod
    def apply_criteria(queryset: QuerySet, criteria: Criteria) -> QuerySet:
        """Apply complete criteria to any queryset"""

        # Apply filters
        if criteria.has_filters():
            queryset = CriteriaConverter._apply_filters(queryset, criteria.filters)

        # Apply ordering
        if criteria.has_orders():
            order_fields = criteria.orders.to_django_order_by()
            queryset = queryset.order_by(*order_fields)

        # Apply projection (select specific fields)
        if criteria.has_projection():
            fields = criteria.projection.to_django_values()
            queryset = queryset.values(*fields)

        # Apply pagination
        if criteria.has_pagination():
            if criteria.offset is not None:
                queryset = queryset[criteria.offset :]
            if criteria.limit is not None:
                end_index = (criteria.offset or 0) + criteria.limit
                start_index = criteria.offset or 0
                queryset = queryset[start_index:end_index]

        return queryset

    @staticmethod
    def _apply_filters(queryset: QuerySet, filters: Filters) -> QuerySet:
        """Apply filters to any queryset"""
        if not filters.filters:
            return queryset

        q_objects = []
        for filter_obj in filters.filters:
            if filter_obj.operator == FilterOperator.AND and filter_obj.nested_filters:
                nested_q = [CriteriaConverter._filter_to_q(nf) for nf in filter_obj.nested_filters]
                combined_q = reduce(operator.and_, nested_q)
                q_objects.append(combined_q)
            elif filter_obj.operator == FilterOperator.OR and filter_obj.nested_filters:
                nested_q = [CriteriaConverter._filter_to_q(nf) for nf in filter_obj.nested_filters]
                combined_q = reduce(operator.or_, nested_q)
                q_objects.append(combined_q)
            else:
                q_objects.append(CriteriaConverter._filter_to_q(filter_obj))

        if q_objects:
            combined_query = reduce(operator.and_, q_objects)
            return queryset.filter(combined_query)

        return queryset

    @staticmethod
    def _filter_to_q(filter_obj: Filter) -> Q:
        """Convert single filter to Django Q object"""
        lookup = filter_obj.to_django_lookup()

        # Handle special exclude cases
        exclude_keys = [key for key in lookup.keys() if key.startswith("_exclude_")]
        if exclude_keys:
            # Create exclude Q object
            exclude_key = exclude_keys[0]
            actual_key = exclude_key.replace("_exclude_", "")
            exclude_value = lookup[exclude_key]
            return ~Q(**{actual_key: exclude_value})

        return Q(**lookup)

