from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Freelancer, Client
from apps.notifications.signals import notificate

# Signal to notify the creation of a Freelancer
@receiver(post_save, sender=Freelancer)
def notify_freelancer_creation(sender, instance, created, **kwargs):
    if created:
        notificate.send(
            sender=instance.user,  # Instance of the Userk model
            destinity=instance.user,  # Instance of the Userk model
            verb=f"A Freelancer account has been created for {instance.user.first_name} {instance.user.last_name}.",
            level='success'
        )

# Signal to notify the creation of a Client
@receiver(post_save, sender=Client)
def notify_client_creation(sender, instance, created, **kwargs):
    if created:
        notificate.send(
            sender=instance.user,  # Instance of the Userk model
            destinity=instance.user,  # Instance of the Userk model
            verb=f"A Client account has been created for {instance.user.first_name} {instance.user.last_name}.",
            level='success'
        )

# Signal to notify the update of a Client
@receiver(post_save, sender=Client)
def notify_client_update(sender, instance, created, **kwargs):
    if not created:  # This means it already existed
        notificate.send(
            sender=instance.user,  # Instance of the Userk model
            destinity=instance.user,  # Instance of the Userk model
            verb=f'Your profile has been updated, {instance.user.first_name} {instance.user.last_name}.',
            level='success'
        )

# Signal to notify the update of a Freelancer
@receiver(post_save, sender=Freelancer)
def notify_freelancer_update(sender, instance, created, **kwargs):
    if not created:  # This means it already existed
        notificate.send(
            sender=instance.user,  # Instance of the Userk model
            destinity=instance.user,  # Instance of the Userk model
            verb=f'Your profile has been updated, {instance.user.first_name} {instance.user.last_name}.',
            level='success'
        )