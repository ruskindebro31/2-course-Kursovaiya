from rest_framework import viewsets, permissions
from rest_framework.response import Response

from .serializers.order_serializer import OrderSerializer, OrderCreateSerializer
from .models import Order


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__candle').all()
        return Order.objects.filter(user=self.request.user).prefetch_related('items__candle')

    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=201)

    def perform_update(self, serializer):
        old_status = self.get_object().status
        order = serializer.save()
        if old_status != order.status:
            from apps.notifications.utils import notify_user
            notify_user(order.user, f'Статус заказа #{order.id} изменён на «{order.status}»')
