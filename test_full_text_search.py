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