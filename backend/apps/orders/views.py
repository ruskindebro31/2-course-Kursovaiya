from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .serializers.order_serializer import OrderSerializer
from .models import Order


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAdminUser()]
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items').all()
        return Order.objects.filter(user=self.request.user).prefetch_related('items')

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        from apps.cart.models.cart import Cart, CartItem
        cart = Cart.objects.filter(user=self.request.user).first()
        if cart:
            cart.items.all().delete()

    def perform_update(self, serializer):
        old_status = self.get_object().status
        order = serializer.save()
        if old_status != order.status:
            from apps.notifications.utils import notify_user, broadcast_notification
            notify_user(order.user, f'Статус заказа #{order.id} изменён на «{order.status}»')
            broadcast_notification(order.user_id, f'Статус заказа #{order.id}: {order.status}')
