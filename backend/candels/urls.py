from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users.views import UserViewSet
from apps.candles.views import CandleViewSet
from apps.orders.views import OrderViewSet
from apps.cart.views import CartViewSet
from apps.reviews.views import ReviewViewSet
from apps.notifications.views import NotificationViewSet
from apps.chat.views import ChatViewSet, MessageViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'candles', CandleViewSet, basename='candle')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'chats', ChatViewSet, basename='chat')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
