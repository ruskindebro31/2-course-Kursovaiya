from rest_framework import serializers
from .models.chat import Chat, Message

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'timestamp', 'is_read']

class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'messages', 'created_at']
