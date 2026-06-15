import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ReviewConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.candle_id = self.scope['url_route']['kwargs']['candle_id']
        self.room_group_name = f'candle_{self.candle_id}_reviews'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def review_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'review',
            'review': event['review'],
        }))
