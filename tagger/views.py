from ordered_set import OrderedSet
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Case, Value, When, Q
from django.contrib.postgres.search import TrigramSimilarity
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.request import clone_request
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView
from tagger import constants
from tagger.models import Category, Mapping, Period
from tagger.serializers import CategorySerializer, MappingSerializer


class MappingBaseView(APIView):
    queryset = Mapping.objects.all()
    serializer_class = MappingSerializer
    active_option_cond = Q(is_option = True) & Q(status__description = constants.Status.ACTIVE)


class MappingBaseListView(MappingBaseView, ListAPIView):
    pass


class MappingBaseRetrieveView(MappingBaseView, RetrieveAPIView):
    pass


class PutAsCreateMixin:
    """
    The following mixin class may be used in order to support
    PUT-as-create behavior for incoming requests.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object_or_none()
        data = {field: value.upper() for field, value in request.data.items()}
        
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)

        status_code = status.HTTP_201_CREATED
        extra_kwargs = {'updated_by': request.user}

        if instance is None:
            extra_kwargs.update({'created_by': request.user})
            status_code = status.HTTP_204_NO_CONTENT

        serializer.save(**extra_kwargs)
        return Response(serializer.data, status = status_code)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def get_object_or_none(self):
        try:
            return self.get_object()
        except Http404:
            if self.request.method == 'PUT':
                # For PUT-as-create operation, we need to ensure that we have
                # relevant permissions, as if this was a POST request. This
                # will either raise a PermissionDenied exception, or simply
                # return None.
                self.check_permissions(clone_request(self.request, 'POST'))
            else:
                # PATCH requests where the object does not exist should still
                # return a 404 response.
                raise


class CategorySearchView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        description = self.request.query_params.get('description')
        if description is not None:
            return self.queryset.annotate(
                search_rank = Case(
                    When(description__iexact = description, then = Value(0)),
                    When(description__istartswith = description, then = Value(1)),
                    When(description__icontains = description, then = Value(2)),
                    default = Value(99),
                )) \
                .exclude(search_rank = 99) \
                .order_by('search_rank')
        return self.queryset


class MappingSearchView(MappingBaseListView):
    
    def get_queryset(self):
        queryset = self.queryset
        description = self.request.query_params.get('description')
        category = self.request.query_params.get('category')

        if category:
            queryset = queryset.filter(code__category__description__iexact = category)

        if description:
            queryset = queryset.annotate(
                search_rank = Case(
                    When(description__description__iexact = description, then = Value(0)),
                    When(description__description__istartswith = description, then = Value(1)),
                    When(description__description__icontains = description, then = Value(2)),
                    default = Value(99),
                )) \
                .filter(~Q(search_rank = 99) & self.active_option_cond) \
                .order_by('search_rank', 'code')
        return queryset
        

class PeriodLookupView(MappingBaseRetrieveView):
    permission_classes = (AllowAny,)
    queryset = Period.objects.all()

    def get_object(self):
        code = self.request.query_params.get('code')
        period = get_object_or_404(self.get_queryset(), icd_input__description__iexact = code)
        code = period.icd_input

        duration = self.request.query_params.get('duration')
        if duration:
            duration = self.validate_duration(duration)
            if duration < period.threshold:
                code = period.icd_below
            elif duration == period.threshold:
                code = period.icd_equal
            else:
                code = period.icd_above
        return code.mappings.get(self.active_option_cond)

    def validate_duration(self, duration):
        try:
            return float(duration)
        except ValueError:
            raise ValidationError({
                "duration": [
                    "Enter a number."
                ]
            })


class MappingExactLookupView(MappingBaseRetrieveView):
    permission_classes = (AllowAny,)

    def get_object(self):
        description = self.request.query_params.get('description')
        filter = {
            'description__description__iexact': description,
            'status__description': constants.Status.ACTIVE,
        }
        obj = get_object_or_404(self.get_queryset(), **filter)
        return self.get_queryset().get(
            Q(code = obj.code) & self.active_option_cond
        )


class MappingFuzzyLookupView(MappingBaseListView):
    permission_classes = (AllowAny,)
    
    def get_queryset(self):
        description = self.request.query_params.get('description')
        if description is not None:
            fuzzy_matches = OrderedSet(
                self.queryset.filter(status__description = constants.Status.ACTIVE) \
                             .annotate(similarity = TrigramSimilarity('description__description', description)) \
                             .filter(similarity__gt = 0.3) \
                             .order_by('-similarity') \
                             .values_list('code', flat = True)
            )
            preserved_order = Case(
                *[When(code = val, then = pos) for pos, val in enumerate(fuzzy_matches)], default = len(fuzzy_matches)
            )
            return self.queryset.filter(Q(code__in = fuzzy_matches) & self.active_option_cond) \
                                .order_by(preserved_order)
        return self.queryset.filter(self.active_option_cond)


class MappingUpdateCreateView(PutAsCreateMixin, MappingBaseView, UpdateAPIView):

    def get_object(self):
        description = self.request.data.get('description')
        filter = {
            'description__description__iexact': description,
            'status__description': constants.Status.PENDING_REVIEW,
            'created_by': self.request.user,
        }
        obj = get_object_or_404(self.get_queryset(), **filter)
        return obj