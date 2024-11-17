from django.db import models
from apps.accounts.models import Freelancer, Client, Userk
import shortuuid
# Create your models here.


class Chat(models.Model):
    chatName = models.CharField(max_length=128, default=shortuuid.uuid)
    freelancer = models.ForeignKey(Freelancer, related_name="chat",blank=True, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name="chat", blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.chatName

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name="chatMessages", on_delete=models.CASCADE)
    author = models.ForeignKey(Userk, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    timeCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} : {self.body}'
    
    class Meta:
        ordering = ['-timeCreated']