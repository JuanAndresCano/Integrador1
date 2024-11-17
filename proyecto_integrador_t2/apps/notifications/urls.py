# urls.py

from django.urls import path
from .views import *
urlpatterns = [
    # Ruta para ver la lista de notificaciones
    path('notifications/', NotificationList.as_view(), name='notifications'),
    
    # Ruta para marcar una notificación como leída
    path('notifications/read/<int:notification_id>/', MarkAsReadView.as_view(), name='mark_as_read'),

    path('notifications/<int:notification_id>/', NotificationDetailView.as_view(), name='notification_detail'),

    
]
