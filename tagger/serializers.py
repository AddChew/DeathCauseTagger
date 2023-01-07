from rest_framework import serializers
from tagger.utils import CustomSlugRelatedField
from tagger.models import Category, Mapping, Code, DeathCause


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