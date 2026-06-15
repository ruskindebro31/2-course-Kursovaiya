from rest_framework import serializers
from ..models import Order

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'total_price', 'status', 'created_at', 'items')
        read_only_fields = ('id', 'user', 'total_price', 'created_at')
