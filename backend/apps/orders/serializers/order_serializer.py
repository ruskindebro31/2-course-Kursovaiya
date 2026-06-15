from rest_framework import serializers

from ..models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    candle_name = serializers.CharField(source='candle.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'candle', 'candle_name', 'quantity', 'price')


class OrderItemCreateSerializer(serializers.Serializer):
    candle = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'total_price', 'status', 'created_at', 'items')
        read_only_fields = ('id', 'user', 'created_at', 'total_price', 'status')


class OrderCreateSerializer(serializers.Serializer):
    items = OrderItemCreateSerializer(many=True)

    def create(self, validated_data):
        user = self.context['request'].user
        items_data = validated_data['items']
        total = sum(i['price'] * i['quantity'] for i in items_data)
        order = Order.objects.create(user=user, total_price=total, status='pending')
        for item in items_data:
            OrderItem.objects.create(
                order=order,
                candle_id=item['candle'],
                quantity=item['quantity'],
                price=item['price'],
            )
        return order
