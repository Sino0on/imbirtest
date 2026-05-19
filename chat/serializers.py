from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'content', 'timestamp', 'sender_username', 'is_read']
        read_only_fields = ['id', 'timestamp']
