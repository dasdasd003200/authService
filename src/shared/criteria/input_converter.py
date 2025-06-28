from .base_criteria import Criteria, Filters, Orders, Filter, Order, Projection, CriteriaOptions, FilterOperator, SortDirection
from .graphql_inputs import CriteriaInput, FilterInput, OrderInput, ProjectionInput, CriteriaOptionsInput, FilterOperatorInput, SortDirectionInput


class CriteriaInputConverter:
    """Converts GraphQL inputs to domain criteria objects - completely generic"""

    @staticmethod
    def from_graphql_input(input_data: CriteriaInput) -> Criteria:
        """Convert GraphQL CriteriaInput to domain Criteria"""

        # Convert filters
        filters = Filters.none()
        if input_data.filters:
            filter_objects = [CriteriaInputConverter._convert_filter(f) for f in input_data.filters]
            filters = Filters(filter_objects)

        # Convert orders
        orders = Orders.none()
        if input_data.orders:
            order_objects = [CriteriaInputConverter._convert_order(o) for o in input_data.orders]
            orders = Orders(order_objects)

        # Convert projection
        projection = None
        if input_data.projection:
            projection = Projection(input_data.projection.fields)

        # Convert options
        options = CriteriaOptions()
        if input_data.options:
            options.explain = input_data.options.explain
            options.comment = input_data.options.comment
            options.batch_size = input_data.options.batch_size

        return Criteria(filters=filters, orders=orders, limit=input_data.limit, offset=input_data.offset, projection=projection, options=options)

    @staticmethod
    def _convert_filter(filter_input: FilterInput) -> Filter:
        """Convert GraphQL filter input to domain filter"""

        # Convert operator
        operator_map = {
            FilterOperatorInput.EQ: FilterOperator.EQ,
            FilterOperatorInput.NE: FilterOperator.NE,
            FilterOperatorInput.GT: FilterOperator.GT,
            FilterOperatorInput.GTE: FilterOperator.GTE,
            FilterOperatorInput.LT: FilterOperator.LT,
            FilterOperatorInput.LTE: FilterOperator.LTE,
            FilterOperatorInput.IN: FilterOperator.IN,
            FilterOperatorInput.NIN: FilterOperator.NIN,
            FilterOperatorInput.CONTAINS: FilterOperator.CONTAINS,
            FilterOperatorInput.ICONTAINS: FilterOperator.ICONTAINS,
            FilterOperatorInput.STARTSWITH: FilterOperator.STARTSWITH,
            FilterOperatorInput.ENDSWITH: FilterOperator.ENDSWITH,
            FilterOperatorInput.ISNULL: FilterOperator.ISNULL,
            FilterOperatorInput.REGEX: FilterOperator.REGEX,
            FilterOperatorInput.AND: FilterOperator.AND,
            FilterOperatorInput.OR: FilterOperator.OR,
        }

        operator = operator_map[filter_input.operator]

        # Handle nested filters for AND/OR
        nested_filters = None
        if filter_input.nested_filters:
            nested_filters = [CriteriaInputConverter._convert_filter(nf) for nf in filter_input.nested_filters]

        return Filter(field=filter_input.field or "", operator=operator, value=filter_input.value, nested_filters=nested_filters)

    @staticmethod
    def _convert_order(order_input: OrderInput) -> Order:
        """Convert GraphQL order input to domain order"""
        direction_map = {SortDirectionInput.ASC: SortDirection.ASC, SortDirectionInput.DESC: SortDirection.DESC}

        return Order(field=order_input.field, direction=direction_map[order_input.direction])
