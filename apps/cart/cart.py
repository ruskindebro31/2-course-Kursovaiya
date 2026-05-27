from decimal import Decimal

from apps.catalog.models import Product


class Cart:
    SESSION_KEY = "cart"

    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(self.SESSION_KEY, {})

    def add(self, product: Product, quantity: int = 1, override_quantity: bool = False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def remove(self, product: Product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session.pop(self.SESSION_KEY, None)
        self.save()

    def save(self):
        self.session[self.SESSION_KEY] = self.cart
        self.session.modified = True

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def __iter__(self):
        if not self.cart:
            return
        product_ids = [int(k) for k in self.cart.keys()]
        products = {str(p.id): p for p in Product.objects.filter(id__in=product_ids, is_active=True)}
        for pid, raw in self.cart.items():
            product = products.get(pid)
            if not product:
                continue
            price = Decimal(str(raw["price"]))
            quantity = int(raw["quantity"])
            yield {
                "product": product,
                "price": price,
                "quantity": quantity,
                "total_price": price * quantity,
            }

    def get_total_price(self):
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())
