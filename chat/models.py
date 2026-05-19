from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    room_name = models.CharField(max_length=255, default='global')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.room_name}] {self.timestamp} - {self.content[:50]}'
