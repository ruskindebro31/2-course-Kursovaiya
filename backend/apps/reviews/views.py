from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from users.permissions import IsOwnerOrReadOnly
from .models.review import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('user', 'candle').all()
    serializer_class = ReviewSerializer
    filterset_fields = ('candle', 'rating')
    search_fields = ('comment',)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsOwnerOrReadOnly()]
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        review = serializer.save(user=self.request.user)
        from apps.reviews.signals import broadcast_review
        broadcast_review(review)

    @action(detail=False, methods=['get'], url_path='by-candle/(?P<candle_id>[^/.]+)')
    def by_candle(self, request, candle_id=None):
        reviews = self.queryset.filter(candle_id=candle_id)
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)
