from rest_framework import serializers
from ..models import Candle, Category


class CategorySerializer(serializers.ModelSerializer):
    candle_count = serializers.IntegerField(source='candles.count', read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'candle_count')


class CandleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Candle
        fields = (
            'id', 'name', 'description', 'price', 'category', 'category_name',
            'image', 'created_at', 'updated_at',
        )
