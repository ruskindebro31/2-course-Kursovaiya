from django.urls import path

from apps.notifications.consumers import NotificationConsumer
from apps.reviews.consumers import ReviewConsumer
from apps.chat.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/notifications/<int:user_id>/', NotificationConsumer.as_asgi()),
    path('ws/reviews/<int:candle_id>/', ReviewConsumer.as_asgi()),
    path('ws/chat/<int:chat_id>/', ChatConsumer.as_asgi()),
]
