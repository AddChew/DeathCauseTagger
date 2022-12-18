from rest_framework import serializers

from tagger.models import Mapping


class MappingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mapping
        fields = (
            'code', 'description'
        )