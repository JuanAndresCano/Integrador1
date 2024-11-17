# Importamos las señales y el modelo de notificación
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.notifications.signals import notificate
from .models import Project
from .models import ProjectContributor, Transaction
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

# Creamos un signal que notifique cuando se cree un proyecto
@receiver(post_save, sender=Project)
def notify_project_created(sender, instance, created, **kwargs):
    if created:
        # Notificación cuando un cliente crea un proyecto
        notificate.send(
            sender=instance.client.user,
            verb=f'created the project "{instance.title}"',
            level='success',
            destinity=instance.client.user,  # Puedes cambiar esto si quieres notificar a otros usuarios
        )


@receiver(post_save, sender=ProjectContributor)
def notify_freelancer_application(sender, instance, **kwargs):
    if instance.is_send:
        if instance.approval_status == "pending" and instance.rejectionReason == "pending":
            notificate.send(
                sender=instance.freelancer.user,
                verb=f'The freelancer {instance.freelancer.user.first_name} {instance.freelancer.user.last_name} has requested to work on your project "{instance.project.title}".',
                level='info',
                destinity=instance.project.client.user,
                url=reverse('fprofileRequest', kwargs={'pk': instance.freelancer.user.id,
                    'contributorId': instance.id})  # Link al perfil del freelancer
            )
        #------------------------------------------------------
        if instance.rejectionReason == "not_rejected":
            notificate.send(
                sender=instance.project.client.user,
                verb=f'The client {instance.project.client.user.first_name} {instance.project.client.user.last_name} has accepted your proposal for the project "{instance.title}". You can now start creating deliverables to submit the proposal.',
                level='success',
                destinity=instance.freelancer.user,
                url=reverse('addDeliverablesProject', kwargs={'pk': instance.id})  # Link al perfil del freelancer
            )
        elif instance.rejectionReason == "profile_rejected":
            notificate.send(
                sender=instance.project.client.user,
                verb=f'The client {instance.project.client.user.first_name} {instance.project.client.user.last_name} has rejected your proposal for the project "{instance.title}". You can send another proposal in 7 days.',
                level='warning',
                destinity=instance.freelancer.user,
            )
        #------------------------------------------------------
        if instance.approval_status == "not_rejected" and instance.rejectionReason == "not_rejected":
            notificate.send(
                sender=instance.freelancer.user,
                verb=f'The freelancer {instance.freelancer.user.first_name} {instance.freelancer.user.last_name} has submitted their proposal with the deliverables for your project "{instance.project.title}".',
                level='info',
                destinity=instance.project.client.user,
                url=reverse('applyProjectFreelancer', kwargs={'pk':instance.id})  # Link al perfil del freelancer
            )
        #------------------------------------------------------
        ''' ESTAS NOTIFICACIONES ESTAN MAL
        if instance.approval_status == "approved":
            notificate.send(
                sender=instance.project.client.user,
                verb=f'Your submitted deliverables for the project "{instance.project.title}" have been accepted. You can check your projects to start working.',
                level='success',
                destinity=instance.freelancer.user,
            )

        if instance.approval_status == "rejected":
            notificate.send(
                sender=instance.project.client.user,
                verb=f'Your submitted deliverables for the project "{instance.project.title}" have been rejected. You can resubmit your proposal by editing the deliverables.',
                level='warning',
                destinity=instance.freelancer.user,
                url=reverse('addDeliverablesProject', kwargs={'pk': instance.id})  # Link al perfil del freelancer
            )
        '''
       #------------------------------------------------------

# Notificación cuando se realiza un pago a un freelancer
@receiver(post_save, sender=Transaction)
def notify_payment_completed(sender, instance, created, **kwargs):
    if created and instance.status == 'completed':
        # Notificación al freelancer
        notificate.send(
            sender=instance.client.user,
            verb=f'Payment for the project "{instance.project.title}" has been completed.',
            level='success',
            destinity=instance.freelancer.user,
            url=reverse('FreelancerFinancialControl')  # Link al control financiero del freelancer
        )
        # Notificación al cliente
        notificate.send(
            sender=instance.freelancer.user,
            verb=f'You have successfully completed the payment for the freelancer {instance.freelancer.user.first_name} {instance.freelancer.user.last_name}.',
            level='success',
            destinity=instance.client.user,
            url=reverse('clientFinancialControl')  # Link al control financiero del cliente
        )
'''
# Notificación cuando un cliente acepta o rechaza la solicitud de un freelancer 
@receiver(post_save, sender=ProjectContributor)
def notify_freelancer_application_response(sender, instance, **kwargs):
    # Activar solo si is_accepted es True, indicando que el cliente ha aceptado la solicitud
    if instance.is_accepted:
        notificate.send(
            sender=instance.project.client.user,
            verb=f'You have accepted the freelancer {instance.freelancer.user.username} to work on your project "{instance.project.title}".',
            level='success',
            destinity=instance.freelancer.user,
            url=reverse('projectDetail', args=[instance.project.id])  # Link al proyecto
        )
    # Activar solo si is_rejected es True, indicando que el cliente ha rechazado la solicitud
    if instance.is_rejected:
        notificate.send(
            sender=instance.project.client.user,
            verb=f'You have rejected the freelancer {instance.freelancer.user.username} to work on your project "{instance.project.title}".',
            level='error',
            destinity=instance.freelancer.user,
            url=reverse('projectDetail', args=[instance.project.id])  # Link al proyecto
        )
'''