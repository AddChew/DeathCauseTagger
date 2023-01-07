from django.urls import re_path, include
from tagger.views import CategorySearchView, MappingSearchView, MappingLookupView, PeriodLookupView


SEARCH_API_PREFIX = 'search'
LOOKUP_API_PREFIX = 'lookup'

search_urlpatterns = [
    re_path(r'^category$', CategorySearchView.as_view(), name = 'category'),
    re_path(r'^mapping$', MappingSearchView.as_view(), name = 'mapping'),
]

lookup_urlpatterns = [
    re_path(r'^mapping$', MappingLookupView.as_view(), name = 'mapping'),
    re_path(r'^period$', PeriodLookupView.as_view(), name = 'period'),
]

urlpatterns = [
    re_path(fr'^{SEARCH_API_PREFIX }/', include((search_urlpatterns, 'search'), namespace = 'search')),
    re_path(fr'{LOOKUP_API_PREFIX}/', include((lookup_urlpatterns, 'lookup'), namespace = 'lookup')),
]