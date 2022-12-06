from django.contrib.postgres.search import TrigramSimilarity, TrigramDistance
from tagger.models import Mapping

test = 'CORONARY HEART DISEASE'

# Similarity
out = Mapping.objects.annotate(
    similarity=TrigramSimilarity('description', test),
).filter(similarity__gt=0.3).order_by('-similarity').values_list('icd__code')[:10]

# # Distance
# Author.objects.annotate(
#     distance=TrigramDistance('name', test),
# ).filter(distance__lte=0.3).order_by('distance')[:10]