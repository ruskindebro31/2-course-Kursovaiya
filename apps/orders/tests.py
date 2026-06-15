from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from apps.catalog.models import Category, Product
from apps.orders.models import Order


class OrderCreateTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Премиум", slug="premium")
        self.product = Product.objects.create(
            category=category,
            name="Свеча Lux",
            slug="lux-candle",
            description="Описание",
            price="1500.00",
            stock=5,
            is_active=True,
        )

    def test_create_order_from_cart(self):
        self.client.post(
            reverse("cart:cart_add", kwargs={"product_id": self.product.id}),
            data={"quantity": 2, "override": False},
        )
        response = self.client.post(
            reverse("orders:order_create"),
            data={
                "full_name": "Иван Иванов",
                "phone": "+79000000000",
                "email": "ivan@example.com",
                "address": "ул. Пушкина, д. 1",
                "comment": "",
                "website": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)

    def test_prefill_form_from_authenticated_user(self):
        user = User.objects.create_user(
            username="vasya",
            email="vasya@example.com",
            password="very-safe-password-123",
            first_name="Василий",
            last_name="Петров",
        )
        self.client.force_login(user)
        self.client.post(
            reverse("cart:cart_add", kwargs={"product_id": self.product.id}),
            data={"quantity": 1, "override": False},
        )

        response = self.client.get(reverse("orders:order_create"))
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertEqual(form["full_name"].value(), "Василий Петров")
        self.assertEqual(form["email"].value(), "vasya@example.com")

    def test_prefill_form_uses_last_order_by_email(self):
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="very-safe-password-123",
            first_name="Мария",
            last_name="Иванова",
        )
        Order.objects.create(
            full_name="Мария Иванова",
            phone="+79990000000",
            email="maria@example.com",
            address="Тверская, 1",
            comment="Позвонить за 30 минут",
        )
        self.client.force_login(user)
        self.client.post(
            reverse("cart:cart_add", kwargs={"product_id": self.product.id}),
            data={"quantity": 1, "override": False},
        )

        response = self.client.get(reverse("orders:order_create"))
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertEqual(form["phone"].value(), "+79990000000")
        self.assertEqual(form["address"].value(), "Тверская, 1")
        self.assertEqual(form["comment"].value(), "Позвонить за 30 минут")
