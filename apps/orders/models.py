from django.core.validators import MinValueValidator
from django.db import models

from apps.catalog.models import Product


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новый"
        PROCESSING = "processing", "В обработке"
        SHIPPED = "shipped", "Отправлен"
        DONE = "done", "Завершен"
        CANCELED = "canceled", "Отменен"

    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} - {self.full_name}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    @property
    def total_price(self):
        return self.price_at_purchase * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
