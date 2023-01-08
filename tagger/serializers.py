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