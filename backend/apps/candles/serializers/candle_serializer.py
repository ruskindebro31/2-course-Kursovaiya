from rest_framework import serializers
from ..models import Candle, Category


class CategorySerializer(serializers.ModelSerializer):
    candle_count = serializers.IntegerField(source='candles.count', read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'is_active', 'candle_count')


class CandleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True, default=None)

    class Meta:
        model = Candle
        fields = (
            'id', 'name', 'description', 'price', 'category', 'category_name',
            'author', 'author_name', 'image', 'is_published', 'created_at', 'updated_at',
        )
        read_only_fields = ('author',)


class CandleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candle
        fields = ('name', 'description', 'price', 'category', 'image', 'is_published')
