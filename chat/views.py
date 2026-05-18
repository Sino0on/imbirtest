from django.shortcuts import render
from rest_framework import generics
from .models import Message
from .serializers import MessageSerializer

def index(request, room_name='global'):
    return render(request, 'index.html', {'room_name': room_name})

class MessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        room_name = self.kwargs.get('room_name', 'global')
        return Message.objects.filter(room_name=room_name).order_by('timestamp')
