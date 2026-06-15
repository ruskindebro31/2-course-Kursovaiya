from rest_framework import serializers

from apps.candles.serializers.candle_serializer import CandleSerializer
from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    candle_detail = CandleSerializer(source='candle', read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'user', 'candle', 'candle_detail', 'created_at')
        read_only_fields = ('user',)
