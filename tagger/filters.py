from ordered_set import OrderedSet
from django.db.models import Case, Value, When, Q, Subquery
from django.contrib.postgres.search import TrigramSimilarity
from django_filters.rest_framework import CharFilter, FilterSet
from tagger import constants
from tagger.models import Status, Category, Mapping


class CategorySearchFilterSet(FilterSet):
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


class MappingSearchFilterSet(FilterSet):
    description = CharFilter(field_name = 'description__description', method = 'filter_query')
    category = CharFilter(field_name = 'code__category__description', lookup_expr = 'iexact')

    def filter_query(self, queryset, name, value):
        active_status = Status.objects.get(description = constants.Status.ACTIVE)
        return queryset.annotate(
            search_rank = Case(
                When(description__description__iexact = value, then = Value(0)),
                When(description__description__istartswith = value, then = Value(1)),
                When(description__description__icontains = value, then = Value(2)),
                default = Value(99),
            )
        ).filter(
            ~Q(search_rank = 99) & Q(is_option = True) & Q(status = active_status)
        ).order_by('search_rank', 'code')

    class Meta:
        model = Mapping
        fields = ('description', 'category')


class MappingLookupFilterSet(FilterSet):
    description = CharFilter(field_name = 'description__description', method = 'filter_query')

    def filter_query(self, queryset, name, value):
        active_status = Status.objects.get(description = constants.Status.ACTIVE)
        exact_match = queryset.filter(description__description__iexact = value) # TODO: account for time period

        if exact_match:
            return queryset.filter(
                Q(code = Subquery(exact_match.values('code'))) & Q(is_option = True) & Q(status = active_status)
            )

        fuzzy_matches = OrderedSet(queryset.filter(
            status = active_status
        ).annotate(
            similarity = TrigramSimilarity('description__description', value)
        ).filter(
            similarity__gt = 0.3
        ).order_by(
            '-similarity'
        ).values_list(
            'code', flat = True
        ))

        preserved_order = Case(
            *[When(code = val, then = pos) for pos, val in enumerate(fuzzy_matches)], default = len(fuzzy_matches)
        )

        return queryset.filter(
            Q(code__in = fuzzy_matches) & Q(status = active_status) & Q(is_option = True)
        ).order_by(preserved_order)