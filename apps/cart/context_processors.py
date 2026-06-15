from apps.cart.cart import Cart


def cart_item_count(request):
    return {"cart_items_count": len(Cart(request))}
