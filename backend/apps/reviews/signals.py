from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def broadcast_review(review):
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return
    async_to_sync(channel_layer.group_send)(
        f'candle_{review.candle_id}_reviews',
        {
            'type': 'review_message',
            'review': {
                'id': review.id,
                'user': review.user.username,
                'rating': review.rating,
                'comment': review.comment,
                'created_at': review.created_at.isoformat(),
            },
        },
    )
