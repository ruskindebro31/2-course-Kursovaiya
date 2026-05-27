from django.test import TestCase
from django.urls import reverse

from apps.catalog.models import Category, Product


class CartFlowTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Классика", slug="classic")
        self.product = Product.objects.create(
            category=category,
            name="Белая свеча",
            slug="white-candle",
            description="Описание",
            price="450.00",
            stock=10,
            is_active=True,
        )

    def test_add_to_cart(self):
        response = self.client.post(
            reverse("cart:cart_add", kwargs={"product_id": self.product.id}),
            data={"quantity": 1, "override": False},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Белая свеча")
