
# ContentType
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

#Timezone
from django.utils import timezone

#load_model
from swapper import load_model

# Signals
from apps.notifications.signals import notificate

#Django
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.db import models

#Models
from apps.accounts.models import Userk



class NotificationQueryset(models.QuerySet):

    def readed(self,include_deleted = True):
        '''
            Retornamos las notificaciones que hayan sido leidas en el actual Queryset    
        '''

        if include_deleted:
            return self.filter(read=True)
        
    def unread(self,include_deleted = False):
        '''
            Retornamos solo los items que no hayan sido leidos en el actual Queryset   
        '''
        if include_deleted==True:
            return self.filter(read=False)
        
    def mark_all_as_readed(self,destinity=None):
        '''
            Marcar todas las notify como leidas en el actual queryset 
        '''
        qs = self.read(False)
        if destinity:
            qs = qs.filter(destinity=destinity)        

        return qs.update(read=True)

    def mark_all_as_not_readed(self,destinity= None):
        '''
            Marcar todas las notify como no leidas en el actual queryset 
        '''
        qs = self.read(True)
        if destinity:
            qs= qs.filter(destinity=destinity)    

        return qs.update(read=False)

class AbstractNotificationManager(models.Manager):
    def get_queryset(self):
        return self.NotificationQueryset(self.Model, using = self._db)

class AbstractNotification(models.Model):
    
    class Levels(models.TextChoices):
        success = 'Success', 'success'
        info = 'Info', 'info',
        wrong = 'Wrong', 'wrong'

    level = models.CharField(choices=Levels.choices,max_length=20,default=Levels.info)

    destinity = models.ForeignKey(Userk, on_delete=models.CASCADE, related_name = 'notifications', blank= True, null= True)

    actor_content_type = models.ForeignKey(ContentType, related_name= 'notication_actor', on_delete= models.CASCADE)
    object_id_actor = models.PositiveIntegerField()
    actor =  GenericForeignKey('actor_content_type','object_id_actor')

    verb = models.CharField(max_length=220)

    read = models.BooleanField(default=False)
    public = models.BooleanField(default=True)
    delete = models.BooleanField(default=False)

    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    url = models.URLField(max_length=200, blank=True, null=True)


    objects = NotificationQueryset.as_manager()

    class Meta:
        abstract = True

    def __str__(self):
        return "Actor: {} --- Destiny: {} --- Verb: {}".format(self.actor.username,self.destinity.username,self.verb)

def notify_signals(verb, **kwargs):
    '''
       Función de controlador para crear una instancia de notificación
       tras una llamada de signal de acción   
    '''
    destinity = kwargs.pop('destinity')  # 'destinity' ya es correcto
    actor = kwargs.pop('sender')
    public = bool(kwargs.pop('public', True))
    timestamp = kwargs.pop('timestamp', timezone.now())
    url = kwargs.pop('url', None)  # Nuevo parámetro opcional para URL

    Notify = load_model('notifications', 'Notification')
    levels = kwargs.pop('level', Notify.Levels.info)

    if isinstance(destinity, Group):
        destinies = destinity.user_set.all()
    elif isinstance(destinity, (QuerySet, list)):
        destinies = destinity
    else:
        destinies = [destinity]

    new_notify = []
    for destinity in destinies:
        notification = Notify(
            destinity=destinity,
            actor_content_type=ContentType.objects.get_for_model(actor),
            object_id_actor=actor.pk,
            verb=str(verb),
            public=public,
            timestamp=timestamp,
            level=levels,
            url=url  # Agrega el URL aquí para asignarlo a la notificación
        )

        notification.save()
        new_notify.append(notification)

    return new_notify


# Conectar la señal
notificate.connect(notify_signals, dispatch_uid='notifications.models.Notification')
