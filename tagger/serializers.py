# from rest_framework import serializers
# from tagger.models import Category, Mapping


# class CategorySerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Category
#         fields = (
#             'description',
#         )


# class MappingSerializer(serializers.ModelSerializer):
#     code = serializers.StringRelatedField()

#     class Meta:
#         model = Mapping
#         fields = (
#             'code', 'description'
#         )