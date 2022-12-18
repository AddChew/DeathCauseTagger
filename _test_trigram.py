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
            SELECT code_id, MAX(SIMILARITY(description, %s)) AS similarity
            FROM tagger_mapping 
            GROUP BY code_id
            HAVING MAX(SIMILARITY(description, 'CORONARY HEART DISEASE')) > 0.3
            ORDER BY similarity DESC
            LIMIT 10  
        """,
        [test] 
        )
        ids = [id[0] for id in cursor.fetchall()]
    return ids

ids = my_custom_sql()

# How to preserve order when using filter __in
preserved = Case(*[When(id=val, then=pos) for pos, val in enumerate(ids)], default=len(ids))
out = Mapping.objects.filter(id__in=ids).order_by(preserved)

# Propose query method for new mapping model
from django.db.models import Q

# This query is wrong
# Produces this: [<Mapping: PULMONARY HEART DISEASE UNSPECIFIED: I279>, <Mapping: HEART DISEASE UNSPECIFIED: I519>, <Mapping: MENINGOCOCCAL HEART DISEASE: A395>, <Mapping: ATHEROSCLEROTIC HEART DISEASE: I251>, <Mapping: KYPHOSCOLIOTIC HEART DISEASE: I271>]
# Expect I251 to be the top option
out = Mapping.objects.filter(is_approved = True) \
                     .annotate(similarity = TrigramSimilarity('description', test)) \
                     .filter(Q(similarity__gt = 0.3) & Q(is_option = True)) \
                     .order_by('-similarity')[:5]

# Expected order (non distinct)
# [<Mapping: CORONARY ARTERY DISEASE: I251>, <Mapping: CORONARY ARTERY DISEASE AND HYPERTENSIVE HEART DISEASE: I251>, <Mapping: HYPERTENSIVE HEART DISEASE AND CORONARY ARTERY DISEASE: I119>, <Mapping: LEFT CORONARY ARTERY DISEASE: I251>, <Mapping: SMALL CORONARY ARTERY DISEASE: I251>]
out = Mapping.objects.filter(is_approved = True) \
                     .annotate(similarity = TrigramSimilarity('description', test)) \
                     .filter(similarity__gt = 0.3) \
                     .order_by('-similarity')[:10]

# Expected order (distinct)
# I251, I119, Q249, I259, I279
# <QuerySet [<Mapping: ATHEROSCLEROTIC HEART DISEASE: I251>, <Mapping: HYPERTENSIVE HEART DISEASE WITHOUT CONGESTIVE HEART FAILURE: I119>, <Mapping: CONGENITAL MALFORMATION OF HEART UNSPECIFIED: Q249>, <Mapping: CHRONIC ISCHAEMIC HEART DISEASE UNSPECIFIED: I259>, <Mapping: PULMONARY HEART DISEASE UNSPECIFIED: I279>, <Mapping: ENDOCARDITIS VALVE UNSPECIFIED: I38X>, <Mapping: ACUTE ISCHAEMIC HEART DISEASE UNSPECIFIED: I249>, <Mapping: RHEUMATIC HEART DISEASE UNSPECIFIED: I099>, <Mapping: HEART DISEASE UNSPECIFIED: I519>, <Mapping: MENINGOCOCCAL HEART DISEASE: A395>]>