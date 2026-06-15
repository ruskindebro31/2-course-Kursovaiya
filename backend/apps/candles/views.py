from rest_framework import viewsets
from .serializers.candle_serializer import CandleSerializer
from .models import Candle

class CandleViewSet(viewsets.ModelViewSet):
    queryset = Candle.objects.all()
    serializer_class = CandleSerializer
    filterset_fields = ('category', 'price', 'material')
    search_fields = ('name', 'description')
    ordering_fields = ('price', 'created_at')
