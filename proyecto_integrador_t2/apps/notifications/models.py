
# Django
from apps.notifications.util.models import AbstractNotification

from apps.accounts.models import Freelancer, Client

from apps.projects.models import *

# Django
from django.db import models

class Notification(AbstractNotification):

    class Meta(AbstractNotification.Meta):
        abstract = False



