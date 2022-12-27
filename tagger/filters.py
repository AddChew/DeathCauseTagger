# from django.db import connection
# from django.db.models import Case, Value, When, Q, Subquery
# from django_filters.rest_framework import CharFilter, FilterSet
# from tagger.models import Category, Mapping


# class CategorySearchFilterSet(FilterSet):
#     description = CharFilter(method = 'filter_query')

#     def filter_query(self, queryset, name, value):
#         return queryset.annotate(
#             search_rank = Case(
#                 When(description__iexact = value, then = Value(0)),
#                 When(description__istartswith = value, then = Value(1)),
#                 When(description__icontains = value, then = Value(2)),
#                 default = Value(99),
#             )
#         ).exclude(
#             search_rank = 99
#         ).order_by('search_rank')

#     class Meta:
#         model = Category
#         fields = ('description',)


# class MappingSearchFilterSet(FilterSet):
#     description = CharFilter(method = 'filter_query')
#     category = CharFilter(field_name = 'code__category__description', lookup_expr = 'iexact')

#     def filter_query(self, queryset, name, value):
#         return queryset.annotate(
#             search_rank = Case(
#                 When(description__iexact = value, then = Value(0)),
#                 When(description__istartswith = value, then = Value(1)),
#                 When(description__icontains = value, then = Value(2)),
#                 default = Value(99),
#             )
#         ).exclude(
#             Q(search_rank = 99) | Q(is_option = False) # TODO: add status active filter also
#         ).order_by('search_rank', 'code')

#     class Meta:
#         model = Mapping
#         fields = ('description', 'category')


# class MappingLookupFilterSet(FilterSet):
#     description = CharFilter(method = 'filter_query')

#     def filter_query(self, queryset, name, value):
#         exact_match = queryset.filter(description__iexact = value)
#         if exact_match:
#             return queryset.filter(
#                 Q(code = Subquery(exact_match.values('code'))) & Q(is_option = True)
#             )

#         # TODO: account for time period # TODO: add status active filter also
#         codes = self.execute_trigram_sql(value)
#         ordered_codes = Case(*[When(code = val, then = pos) for pos, val in enumerate(codes)], default = len(codes))
#         return queryset.filter(
#                 Q(code__in = codes) & Q(is_option = True)
#             ).order_by(ordered_codes)

#     def execute_trigram_sql(self, value):
#         with connection.cursor() as cursor:
#             cursor.execute(
#             """
#             SELECT code_id, MAX(SIMILARITY(description, %(description)s)) AS similarity
#             FROM tagger_mapping 
#             GROUP BY code_id
#             HAVING MAX(SIMILARITY(description, %(description)s)) > 0.3
#             ORDER BY similarity DESC 
#             """,
#             {'description': value},
#             )
#             return [code[0] for code in cursor.fetchall()]

#     class Meta:
#         model = Mapping
#         fields = ('description',)