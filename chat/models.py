from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class ChatRoom(models.Model):

    room_name = models.CharField(max_length=1000)
    user1 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user2')