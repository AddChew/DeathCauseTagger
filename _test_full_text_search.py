from django.contrib.postgres.search import SearchVector
from tagger.models import Mapping

test = 'CORONARY HEART DISEASE'

# Single field search ---> its actually pretty decent for cases with missing words and no spelling errors
# Full text search will fail in the case of spelling errors
out = Mapping.objects.filter(description__search=test)

# Multiple field search
out = Mapping.objects.annotate(search=SearchVector("description", "icd__description")).filter(search=test)

# Combine searchvector, searchquery and searchrank ---> use this for search dropdown list
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline

search_query = SearchQuery(test)
search_vector = SearchVector("description", "icd__description")
out = Mapping.objects.annotate(
    search=search_vector, rank=SearchRank(search_vector, search_query)
).filter(search=search_query
).order_by("-rank")

# SearchHeadline ---> returns a headline with the search terms highlighted
# out[0].headline ---> '<b>CHRONIC</b> <b>ISCHAEMIC</b> HEART DISEASE'
# out[2].headline ---> '<b>ISCHAEMIC</b> HEART DISEASE AND <b>CHRONIC</b> KIDNEY DISEASE'
search_headline = SearchHeadline("description", search_query)
out = Mapping.objects.annotate(
    search=search_vector,
    rank=SearchRank(search_vector, search_query)
).annotate(headline=search_headline).filter(search=search_query).order_by("-rank")

# Ways to boost performance

# 1. Save the search vectors to the database with SearchVectorField. Instead of converting the strings to search vectors on the fly
# we create a separate field that contains the processed search vectors and update the field any time there is an insert or update to the description fields
# https://testdriven.io/blog/django-search/#search-vector-field

# 2. Create a database index, i.e. GinIndex


# Search with GinIndex
out = Mapping.objects.filter(search_vector='CORONARY HEART DISEASE').values_list('icd__code', 'icd__description')

search_query = SearchQuery('CORONARY HEART DISEASE') | SearchQuery('CHRONIC HEART DISEASE')
# search_query = SearchQuery('CORONARY HEART DISEASE') & SearchQuery('CHRONIC HEART DISEASE')
# search_query = ~SearchQuery('CORONARY HEART DISEASE')
out = Mapping.objects.filter(search_vector=search_query) # SearchQuery allows you to combine queries with an AND/OR/NOT operator

# Rank and Order
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import F

query = SearchQuery('CORONARY HEART DISEASE')

# The first argument should be a search vector field. It can be either a SearchVector instance or an F() expression. 
# A SearchVector instance computes search vectors from other columns on-the-fly. 
# On the other hand, an F() expression refers an existing search vector field in a model.
rank = SearchRank(F('search_vector'), query)
out = Mapping.objects.annotate(rank=rank).filter(search_vector=query).order_by('-rank')