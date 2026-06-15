from rest_framework import serializers
from .models.review import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'candle', 'rating', 'comment', 'created_at']
        read_only_fields = ['user']
