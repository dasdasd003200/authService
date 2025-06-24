# src/core/domain/repositories/criteria/text_search_criteria.py - CORREGIDO
from typing import List

# from functools import reduce
# import operator
from django.db.models import QuerySet, Q
from ..base_criteria import BaseCriteria


class TextSearchCriteria(BaseCriteria):
    """Criteria for text search across multiple fields"""

    def __init__(self, search_term: str, fields: List[str]):
        self.search_term = search_term.strip()
        self.fields = fields

    def apply(self, queryset: QuerySet) -> QuerySet:
        if not self.search_term:
            return queryset

        # CORREGIDO: Método más robusto que evita problemas de tipos con Django
        if not self.fields:
            return queryset

        # Crear lista de Q objects
        q_objects = []
        for field in self.fields:
            q_objects.append(Q(**{f"{field}__icontains": self.search_term}))

        # Combinar todos los Q objects con OR
        if q_objects:
            # Usar reduce para combinar múltiples Q objects
            from functools import reduce
            import operator

            combined_query = reduce(operator.or_, q_objects)
            return queryset.filter(combined_query)

        return queryset

    def to_dict(self) -> dict:
        return {
            "type": "text_search",
            "search_term": self.search_term,
            "fields": self.fields,
        }
