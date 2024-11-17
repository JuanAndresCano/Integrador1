from django.test import SimpleTestCase
from django.urls import reverse, resolve
from apps.notifications.views import *

class TestUrls(SimpleTestCase):

    # Test para la URL de la lista de notificaciones
    def testUrlNotificationList(self):
        url = reverse('notifications')
        self.assertEqual(resolve(url).func.view_class, NotificationList)

    # Test para la URL de marcar notificación como leída
    def testUrlMarkAsRead(self):
        url = reverse('mark_as_read', args=[1])  # Usa un ID de ejemplo
        self.assertEqual(resolve(url).func.view_class, MarkAsReadView)

    # Test para la URL del detalle de la notificación
    def testUrlNotificationDetail(self):
        url = reverse('notification_detail', args=[1])  # Usa un ID de ejemplo
        self.assertEqual(resolve(url).func.view_class, NotificationDetailView)
