from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from tagger import constants
from tagger.models import Category, Mapping, Period
from tagger.utils import PutAsCreateMixin
from tagger.serializers import CategorySerializer, MappingSerializer
from tagger.filters import CategorySearchFilterSet, MappingSearchFilterSet, MappingLookupFilterSet, PeriodLookupFilterSet


class CategorySearchView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_class = CategorySearchFilterSet


class MappingSearchView(ListAPIView):
    queryset = Mapping.objects.all()
    serializer_class = MappingSerializer
    filterset_class = MappingSearchFilterSet


class PeriodLookupView(ListAPIView):
    queryset = Period.objects.all()
    serializer_class = MappingSerializer
    filterset_class = PeriodLookupFilterSet


class MappingLookupView(ListAPIView, PutAsCreateMixin, UpdateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Mapping.objects.all()
    serializer_class = MappingSerializer
    filterset_class = MappingLookupFilterSet

    def get_object(self):
        description = self.request.data.get('description')
        if isinstance(description, str):
            description = description.upper()

        filter = {
            'description__description': description,
            'status__description': constants.Status.PENDING_REVIEW,
            'created_by': self.request.user 
        }
        obj = get_object_or_404(self.get_queryset(), **filter)
        return obj