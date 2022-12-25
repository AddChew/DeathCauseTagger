from django.urls import re_path, include
from tagger.views import CategorySearchView, MappingSearchView


SEARCH_API_PREFIX = 'search'
# LOOKUP_API_PREFIX = 'lookup'

search_urlpatterns = [
    re_path(r'^category$', CategorySearchView.as_view(), name = 'category'),
    re_path(r'^mapping$', MappingSearchView.as_view(), name = 'mapping'),
]

urlpatterns = [
     re_path(fr'^{SEARCH_API_PREFIX }/', include((search_urlpatterns, 'search'), namespace = 'search')),
]
