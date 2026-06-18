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
    image = serializers.SerializerMethodField()

    class Meta:
        model = Candle
        fields = (
            'id', 'name', 'description', 'price', 'category', 'category_name',
            'season', 'author', 'author_name', 'image', 'is_published', 'created_at', 'updated_at',
        )
        read_only_fields = ('author',)

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        url = obj.image.url
        if request is not None:
            return request.build_absolute_uri(url)
        return url


class CandleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candle
        fields = ('name', 'description', 'price', 'category', 'season', 'image', 'is_published')
