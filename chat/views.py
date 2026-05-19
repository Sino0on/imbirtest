from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer

@login_required
def index(request, room_name='global'):
    return render(request, 'index.html', {'room_name': room_name})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            user, created = User.objects.get_or_create(username=username)
            login(request, user)
            return redirect('index', room_name='global')
    return render(request, 'login.html')

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        if not username:
            return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
        user, created = User.objects.get_or_create(username=username)
        login(request, user)  # Это установит sessionid куки для фронтенда
        return Response({
            "message": "Logged in successfully",
            "username": user.username,
            "id": user.id
        })


class MessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        room_name = self.kwargs.get('room_name', 'global')
        return Message.objects.filter(room_name=room_name).order_by('timestamp')
