from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from apps.cart.cart import Cart
from apps.orders.forms import OrderCreateForm
from apps.orders.models import Order, OrderItem


def _get_order_initial_for_user(request):
    if not request.user.is_authenticated:
        return {}

    user = request.user
    full_name = f"{user.first_name} {user.last_name}".strip() or user.get_username()
    initial = {
        "full_name": full_name,
        "email": user.email or "",
    }

    if user.email:
        last_order = Order.objects.filter(email__iexact=user.email).order_by("-created_at").first()
        if last_order:
            initial.update(
                {
                    "full_name": last_order.full_name or initial["full_name"],
                    "phone": last_order.phone,
                    "address": last_order.address,
                    "comment": last_order.comment,
                }
            )
    return initial


@require_http_methods(["GET", "POST"])
def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Корзина пуста.")
        return redirect("core:home")

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                full_name=form.cleaned_data["full_name"],
                phone=form.cleaned_data["phone"],
                email=form.cleaned_data["email"],
                address=form.cleaned_data["address"],
                comment=form.cleaned_data["comment"],
            )
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    price_at_purchase=item["price"],
                )
            cart.clear()
            return render(request, "orders/created.html", {"order": order})
    else:
        form = OrderCreateForm(initial=_get_order_initial_for_user(request))

    return render(request, "orders/create.html", {"cart": cart, "form": form})
