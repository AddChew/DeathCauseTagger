from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from tagger.models import Status, Category, Mapping
from tagger.serializers import CategorySerializer, MappingSerializer
from tagger.filters import CategorySearchFilterSet, MappingSearchFilterSet, MappingSingleLookupFilterSet


class CategorySearchView(ListAPIView):
    # permission_classes = (IsAuthenticated,) # TODO: Uncomment out for actual production
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_class = CategorySearchFilterSet


class MappingSearchView(ListAPIView):
    # permission_classes = (IsAuthenticated,) # TODO: Uncomment out for actual production
    queryset = Mapping.objects.all()
    serializer_class = MappingSerializer
    filterset_class = MappingSearchFilterSet


class MappingSingleLookupView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Mapping.objects.all()
    serializer_class = MappingSerializer
    filterset_class = MappingSingleLookupFilterSet