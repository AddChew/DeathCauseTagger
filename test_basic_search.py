from django.db.models import Q
from tagger.models import Mapping

test = 'CORONARY HEART DISEASE'

# Exact match using filter ---> returns a queryset even if there is only one match
out = Mapping.objects.filter(
    Q(description=test) | Q(icd__description=test) # filter for mappings with description = test or icd = test
)

# Exact match using get ---> returns only a single object
# will raise a Object.DoesNotExist error if there is no matching object or a MultipleObjectsReturned error if there are more than one matches
out = Mapping.objects.get(
    Q(description=test) | Q(icd__description=test)
)

# Contains search
out = Mapping.objects.filter(
    Q(description__icontains=test) | Q(icd__description__icontains=test) # filter for mappings with description containing test or icd containing test
)