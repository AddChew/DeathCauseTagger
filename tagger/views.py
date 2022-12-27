# from rest_framework.generics import ListAPIView
# from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
# from tagger.models import Category, Mapping
# from tagger.filters import CategorySearchFilterSet, MappingSearchFilterSet, MappingLookupFilterSet
# from tagger.serializers import MappingSerializer, CategorySerializer


# class CategorySearchView(ListAPIView):
#     # permission_classes = (IsAuthenticated,) # TODO: Uncomment out for actual production
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     filterset_class = CategorySearchFilterSet


# class MappingSearchView(ListAPIView):
#     # permission_classes = (IsAuthenticated,) # TODO: Uncomment out for actual production
#     queryset = Mapping.objects.all()
#     serializer_class = MappingSerializer
#     filterset_class = MappingSearchFilterSet


# class MappingLookupView(ListAPIView):
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     queryset = Mapping.objects.all()
#     serializer_class = MappingSerializer
#     filterset_class = MappingLookupFilterSet



# class MappingsView(APIView):
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

#     def get(self, request, *args, **kwargs):
#         pass