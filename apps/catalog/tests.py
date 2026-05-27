from django.test import TestCase
from django.urls import reverse

from apps.catalog.models import Category, Product


class CatalogViewsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Ароматические", slug="aroma")
        self.product = Product.objects.create(
            category=self.category,
            name="Ванильная свеча",
            slug="vanilla-candle",
            description="Описание",
            price="990.00",
            stock=10,
            is_active=True,
        )

    def test_product_list_redirects_to_home(self):
        response = self.client.get(reverse("catalog:product_list"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("core:home"))

    def test_home_lists_active_products(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_detail_page_returns_200(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
