# apps/notifications/context_processors.py
from swapper import load_model

NotificationK = load_model('notifications', 'Notification')

def unread_notifications(request):
    """
    Retorna el conteo de notificaciones no leídas del usuario.
    Se incluye en el contexto de todas las plantillas.
    """
    if request.user.is_authenticated:
        unread_count = NotificationK.objects.filter(destinity=request.user, read=False).count()
    else:
        unread_count = 0
    
    return {'unread_count': unread_count}
