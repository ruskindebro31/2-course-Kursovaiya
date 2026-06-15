from rest_framework import serializers

from ..models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    candle_name = serializers.CharField(source='candle.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'candle', 'candle_name', 'quantity', 'price')


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'total_price', 'status', 'created_at', 'items')
        read_only_fields = ('id', 'user', 'created_at')
