from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView

from apps.candles.views import CandleViewSet, CategoryViewSet
from apps.orders.views import OrderViewSet
from apps.cart.views import CartViewSet
from apps.reviews.views import ReviewViewSet
from apps.notifications.views import NotificationViewSet
from apps.chat.views import ChatViewSet, MessageViewSet
from apps.favorites.views import FavoriteViewSet

admin.site.site_header = 'Candels — администрирование'
admin.site.site_title = 'Candels Admin'
admin.site.index_title = 'Управление интернет-магазином свечей'

try:
    from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
    admin.site.unregister(BlacklistedToken)
    admin.site.unregister(OutstandingToken)
except admin.sites.NotRegistered:
    pass

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'candles', CandleViewSet, basename='candle')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'chats', ChatViewSet, basename='chat')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'favorites', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', RedirectView.as_view(url='/api/docs/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('users.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
