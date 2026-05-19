import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        if self.user.is_authenticated:
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

            # Broadcast user joined
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_join',
                    'username': self.user.username,
                }
            )
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            # Broadcast user left
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_leave',
                    'username': self.user.username,
                }
            )
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msg_type = text_data_json.get('type', 'chat_message')

        if msg_type == 'chat_message':
            message_content = text_data_json['message']
            # Save message to database
            saved_message = await self.save_message(message_content)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message_id': saved_message.id,
                    'message': saved_message.content,
                    'timestamp': str(saved_message.timestamp),
                    'sender_username': self.user.username,
                }
            )
        elif msg_type == 'typing':
            # Send typing status to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_typing',
                    'username': self.user.username,
                    'is_typing': text_data_json.get('is_typing', True),
                }
            )
        elif msg_type == 'read':
            message_id = text_data_json.get('message_id')
            if message_id:
                await self.mark_message_read(message_id)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'message_read',
                        'message_id': message_id,
                        'reader_username': self.user.username,
                    }
                )

    # Receive message from room group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message_id': event['message_id'],
            'message': event['message'],
            'timestamp': event.get('timestamp', ''),
            'sender_username': event.get('sender_username', ''),
        }))

    async def user_join(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_join',
            'username': event['username'],
        }))

    async def user_leave(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_leave',
            'username': event['username'],
        }))

    async def user_typing(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'username': event['username'],
            'is_typing': event['is_typing'],
        }))

    async def message_read(self, event):
        await self.send(text_data=json.dumps({
            'type': 'read',
            'message_id': event['message_id'],
            'reader_username': event['reader_username'],
        }))

    @database_sync_to_async
    def save_message(self, content):
        return Message.objects.create(room_name=self.room_name, content=content, sender=self.user)

    @database_sync_to_async
    def mark_message_read(self, message_id):
        try:
            msg = Message.objects.get(id=message_id)
            if not msg.is_read:
                msg.is_read = True
                msg.save()
        except Message.DoesNotExist:
            pass
