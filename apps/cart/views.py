from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.cart.cart import Cart
from apps.cart.forms import CartAddProductForm
from apps.catalog.models import Product


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/detail.html", {"cart": cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cart.add(
            product=product,
            quantity=form.cleaned_data["quantity"],
            override_quantity=form.cleaned_data["override"],
        )
        messages.success(request, "Товар добавлен в корзину.")
    return redirect("core:home")


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, "Товар удален из корзины.")
    return redirect("cart:cart_detail")
