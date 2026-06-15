from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models.notification import Notification


def notify_user(user, message):
    notification = Notification.objects.create(user=user, message=message)
    broadcast_notification(user.id, message)
    return notification


def broadcast_notification(user_id, message):
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return
    async_to_sync(channel_layer.group_send)(
        f'notifications_{user_id}',
        {
            'type': 'notification_message',
            'message': message,
        },
    )
