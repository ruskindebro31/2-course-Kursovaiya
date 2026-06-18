from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from users.permissions import IsAuthorOrReadOnly
from .models import Candle, Category
from .serializers.candle_serializer import (
    CandleSerializer, CategorySerializer, CandleCreateSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class CandleViewSet(viewsets.ModelViewSet):
    queryset = Candle.objects.filter(is_published=True).select_related('category', 'author')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ('category', 'price', 'season')
    search_fields = ('name', 'description')
    ordering_fields = ('price', 'created_at', 'name')

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return CandleCreateSerializer
        return CandleSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAuthorOrReadOnly()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = Candle.objects.select_related('category', 'author')
        if self.action in ('update', 'partial_update', 'destroy', 'retrieve'):
            return qs
        if self.request.user.is_staff:
            return qs
        return qs.filter(is_published=True)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = CandleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        candle = serializer.save(author=request.user)
        return Response(
            CandleSerializer(candle, context={'request': request}).data,
            status=201,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = CandleCreateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        candle = serializer.save()
        return Response(CandleSerializer(candle, context={'request': request}).data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def mine(self, request):
        candles = self.queryset.filter(author=request.user)
        page = self.paginate_queryset(candles)
        if page is not None:
            serializer = CandleSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = CandleSerializer(candles, many=True, context={'request': request})
        return Response(serializer.data)
