from ordered_set import OrderedSet
from django.http import Http404
from django.db.models import Case, Value, When, Q, Subquery
from django.contrib.postgres.search import TrigramSimilarity
from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter
from tagger import constants
from tagger.utils import BaseMappingFilterSet
from tagger.models import Category, Mapping, Period


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


class MappingSearchFilterSet(BaseMappingFilterSet):
    description = CharFilter(field_name = 'description__description', method = 'filter_query')
    category = CharFilter(field_name = 'code__category__description', lookup_expr = 'iexact')

    def filter_query(self, queryset, name, value):
        return queryset.annotate(
            search_rank = Case(
                When(description__description__iexact = value, then = Value(0)),
                When(description__description__istartswith = value, then = Value(1)),
                When(description__description__icontains = value, then = Value(2)),
                default = Value(99),
            )
        ).filter(
            ~Q(search_rank = 99) & self.active_option_cond
        ).order_by('search_rank', 'code')

    class Meta:
        model = Mapping
        fields = ('description', 'category')


class PeriodLookupFilterSet(BaseMappingFilterSet):
    code = CharFilter(field_name = 'icd_input__description', lookup_expr = 'iexact')
    duration = NumberFilter(method = 'filter_duration', label = 'Duration')

    def filter_duration(self, queryset, name, value):
        if queryset:
            period = queryset.first()
            if value < period.threshold:
                code = period.icd_below
            elif value == period.threshold:
                code = period.icd_equal
            else:
                code = period.icd_above
            return code.mappings.filter(self.active_option_cond)
        raise Http404

    class Meta:
        model = Period
        fields = ('code', 'duration')


class MappingLookupFilterSet(BaseMappingFilterSet):
    description = CharFilter(field_name = 'description__description', method = 'filter_description', label = 'Description')

    def filter_description(self, queryset, name, value):
        exact_match = queryset.filter(description__description__iexact = value)
        exact_match_option = queryset.filter(
            Q(code = Subquery(exact_match.values('code'))) & self.active_option_cond
        )
        if exact_match_option:
            return exact_match_option

        fuzzy_matches = OrderedSet(queryset.filter(
            status__description = constants.Status.ACTIVE
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
            Q(code__in = fuzzy_matches) & self.active_option_cond
        ).order_by(preserved_order)

    class Meta:
        model = Mapping
        fields = ('description',) 