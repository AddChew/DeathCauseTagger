from django.contrib import admin

from base.admin import BaseAdmin
from categories.models import Category


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    """
    Admin Class for Category Model.
    """
    pass