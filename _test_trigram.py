from django.contrib.postgres.search import TrigramSimilarity, TrigramDistance
from tagger.models import Mapping, ICD

test = 'CORONARY HEART DISEASE'

# Similarity
out = Mapping.objects.annotate(
    similarity=TrigramSimilarity('description', test),
).filter(similarity__gt=0.3).order_by('-similarity')[:10]

out = Mapping.objects.annotate(
    similarity=TrigramSimilarity('description', test),
).filter(similarity__gt=0.3).order_by('-similarity').values_list('icd__code')[:10]

# # Distance
# Author.objects.annotate(
#     distance=TrigramDistance('name', test),
# ).filter(distance__lte=0.3).order_by('distance')[:10]

# Use custom SQL queries
from django.db import connection
from django.db.models import Case, When

def my_custom_sql():
    with connection.cursor() as cursor:
        cursor.execute(
        """
            SELECT icd_id, MAX(SIMILARITY(description, 'CORONARY HEART DISEASE')) AS similarity
            FROM tagger_mapping 
            GROUP BY icd_id
            HAVING MAX(SIMILARITY(description, 'CORONARY HEART DISEASE')) > 0.3
            ORDER BY similarity DESC
            LIMIT 10  
        """  
        )
        ids = [id[0] for id in cursor.fetchall()]
    return ids

ids = my_custom_sql()

# How to preserve order when using filter __in
preserved = Case(*[When(id=val, then=pos) for pos, val in enumerate(ids)], default=len(ids))
out = ICD.objects.filter(id__in=ids).order_by(preserved)

# Propose query method for new mapping model
from django.db.models import Q

out = Mapping.objects.filter(is_approved = True) \
                     .annotate(similarity = TrigramSimilarity('description', test)) \
                     .filter(Q(similarity__gt = 0.3) & Q(is_option = True)) \
                     .order_by('-similarity')[:5]