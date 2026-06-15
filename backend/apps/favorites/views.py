from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Favorite
from .serializers import FavoriteSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('candle', 'candle__category')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='toggle')
    def toggle(self, request):
        candle_id = request.data.get('candle')
        if not candle_id:
            return Response({'detail': 'candle is required'}, status=status.HTTP_400_BAD_REQUEST)
        favorite = Favorite.objects.filter(user=request.user, candle_id=candle_id).first()
        if favorite:
            favorite.delete()
            return Response({'favorited': False, 'candle': candle_id})
        favorite = Favorite.objects.create(user=request.user, candle_id=candle_id)
        serializer = self.get_serializer(favorite)
        return Response({'favorited': True, **serializer.data}, status=status.HTTP_201_CREATED)
