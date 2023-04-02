from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from tagger.models import Category, Mapping, Code, DeathCause


class CustomSlugRelatedField(serializers.SlugRelatedField):

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except ObjectDoesNotExist:
            return self.get_queryset().create(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail('Invalid data type or value.')


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = (
            'description',
        )


class MappingSerializer(serializers.ModelSerializer):
    code = serializers.SlugRelatedField(slug_field = 'description', queryset = Code.objects.all())
    description = CustomSlugRelatedField(slug_field = 'description', queryset = DeathCause.objects.all())

    class Meta:
        model = Mapping
        fields = (
            'code', 'description'
        )


class DeathCausesSerializer(serializers.Serializer):
    description = serializers.ListField(child = serializers.CharField(max_length = 200), allow_empty = False)
    duration = serializers.ListField(child = serializers.DecimalField(max_digits = 7, decimal_places = 2, min_value = 0, coerce_to_string = False), allow_empty = False)

    def validate(self, attrs):
        if len(attrs['description']) != len(attrs['duration']):
            raise serializers.ValidationError('Number of descriptions must match number of durations.')
        return super().validate(attrs)