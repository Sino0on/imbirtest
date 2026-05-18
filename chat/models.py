from django.db import models

class Message(models.Model):
    room_name = models.CharField(max_length=255, default='global')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.room_name}] {self.timestamp} - {self.content[:50]}'
