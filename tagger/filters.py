from django.db.models import Case, Value, When, Q
from django_filters.rest_framework import CharFilter, FilterSet
from tagger.models import Category, Mapping


class CategoryFilterSet(FilterSet):
    description = CharFilter(method = 'filter_query')

    def filter_query(self, queryset, name, value):
        return queryset.annotate(
            search_rank = Case(
                When(description__iexact = value, then = Value(0)),
                When(description__istartswith = value, then = Value(1)),
                When(description__icontains = value, then = Value(2)),
                default = Value(99),
            )
        ).exclude(
            search_rank = 99
        ).order_by('search_rank')

    class Meta:
        model = Category
        fields = ('description',)


class MappingFilterSet(FilterSet):
    description = CharFilter(method = 'filter_query')
    category = CharFilter(field_name = 'code__category__description', lookup_expr = 'iexact')

    def filter_query(self, queryset, name, value):
        return queryset.annotate(
            search_rank = Case(
                When(description__iexact = value, then = Value(0)),
                When(description__istartswith = value, then = Value(1)),
                When(description__icontains = value, then = Value(2)),
                default = Value(99),
            )
        ).exclude(
            Q(search_rank = 99) | Q(is_option = False)
        ).order_by('search_rank', 'code')

    class Meta:
        model = Mapping
        fields = ('description', 'category')