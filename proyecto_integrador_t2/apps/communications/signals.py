from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from .models import Message
from apps.notifications.signals import notificate

# Señal para notificar cuando se envía un mensaje
@receiver(post_save, sender=Message)
def notify_message_sent(sender, instance, created, **kwargs):
    if created:
        # Determinar el destinatario de la notificación
        chat = instance.chat
        
        # Identificar si el destinatario es el cliente o el freelancer
        if instance.author == chat.client.user:  # Si el autor es el cliente, notificar al freelancer
            recipient = chat.freelancer.user
            chat_url = reverse('freelancerMessage', kwargs={'chatName': chat.chatName})  # URL para freelancer
        else:  # Si el autor es el freelancer, notificar al cliente
            recipient = chat.client.user
            chat_url = reverse('clientMessage', kwargs={'chatName': chat.chatName})  # URL para cliente

        # Enviar notificación al destinatario con la URL incluida
        notificate.send(
            sender=instance.author,  # Quien envía el mensaje
            destinity=recipient,  # Destinatario de la notificación
            verb=f'Te ha enviado un mensaje: {instance.body[:30]}...',  # El contenido del mensaje recortado para la notificación
            level='info',
            url=chat_url  # URL para redirigir al chat específico
        )
