from ninja import ModelSchema

from categories.models import Category


class CategorySchema(ModelSchema):
    """
    Category Schema.
    """
    class Meta:
        model = Category
        fields = ["description"]
