from django.test import TestCase
from django.test.client import Client

from mainapp.models import ProductCategory, Product


class TestMainappSmoke(TestCase):
    status_code_success = 200

    def setUp(self):
        cat_1 = ProductCategory.objects.create(
            name='cat 1'
        )
        for i in range(50):
            Product.objects.create(
                category=cat_1,
                name=f'prod {i}'
            )
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)

    def test_products_url(self):
        for product_item in Product.objects.all():
            response = self.client.get(f'/product/{product_item.pk}/')
            self.assertEqual(response.status_code, self.status_code_success)
