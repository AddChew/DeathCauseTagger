from django.test import TestCase

# Create your tests here.
from tagger.models import Category

class CategoryTestCase(TestCase):

    def setUp(self):
        category1 = Category.objects.create(description = 'category1')

    def test_category(self):
        category = Category.objects.get(pk = 1)
        self.assertEqual(category.description, "category1")