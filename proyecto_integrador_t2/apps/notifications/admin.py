from django.contrib import admin

# Django
from apps.notifications.util.admin import AbstractNotifyAdmin

# Models
from .models import Notification

admin.site.register(Notification, AbstractNotifyAdmin)