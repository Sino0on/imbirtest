from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.index, name='index'),
    path('<str:room_name>/', views.index, name='room'),
    path('api/login/', views.LoginAPIView.as_view(), name='api-login'),
    path('api/messages/', views.MessageListAPIView.as_view(), name='message-list'),
    path('api/messages/<str:room_name>/', views.MessageListAPIView.as_view(), name='message-list-room'),
]
