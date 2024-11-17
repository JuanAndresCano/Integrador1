from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from swapper import load_model

NotificationK = load_model('notifications', 'Notification')

class NotificationList(ListView):
    model = NotificationK
    template_name = 'notify.html'
    context_object_name = 'notify'

    @method_decorator(login_required)
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self) -> QuerySet[Any]:
        # Obtener el parámetro de filtro de la solicitud
        filter_type = self.request.GET.get('filter', 'pending')

        # Filtrar las notificaciones según el tipo seleccionado
        if filter_type == 'read':
            return self.request.user.notifications.filter(read=True).order_by('-timestamp')
        elif filter_type == 'all':
            return self.request.user.notifications.all().order_by('-timestamp')
        else:  # Por defecto, mostrar solo las no leídas
            return self.request.user.notifications.filter(read=False).order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Contar las notificaciones no leídas
        context['unread_count'] = self.request.user.notifications.filter(read=False).count()
        return context
    

@method_decorator(login_required, name='dispatch')
class MarkAsReadView(View):
    
    def get(self, request, notification_id, *args, **kwargs):
        # Obtén la notificación específica del usuario
        notification = get_object_or_404(NotificationK, id=notification_id, destinity=request.user)
        
        # Marca la notificación como leída
        notification.read = True
        notification.save()

        # Redirige a la página de notificaciones
        return redirect('notifications')  # Asegúrate de que esta URL esté definida correctamente
    
@method_decorator(login_required, name='dispatch')
class NotificationDetailView(View):
    def get(self, request, notification_id, *args, **kwargs):
        notification = get_object_or_404(NotificationK, id=notification_id, destinity=request.user)
        notification.read = True
        notification.save()
        
        return redirect(notification.url)




    

'''
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from apps.projects.models import Project, RequestList, ProjectContributor  # Ajusta según tu modelo real

def approve_freelancer_request(request, project_id, freelancer_id):
    # Obtén el proyecto y la solicitud del freelancer
    project = get_object_or_404(Project, id=project_id)
    freelancer_request = get_object_or_404(RequestList, project=project, freelancer_id=freelancer_id)

    # Agregar al freelancer como colaborador del proyecto
    ProjectContributor.objects.create(project=project, freelancer=freelancer_request.freelancer)

    # Opcional: Eliminar la solicitud de freelancer
    freelancer_request.delete()

    messages.success(request, "Freelancer approved successfully!")
    return redirect('notify')  # Redirige a la página de notificaciones

def reject_freelancer_request(request, project_id, freelancer_id):
    # Obtén el proyecto y la solicitud del freelancer
    project = get_object_or_404(Project, id=project_id)
    freelancer_request = get_object_or_404(RequestList, project=project, freelancer_id=freelancer_id)

    # Opcional: Eliminar la solicitud de freelancer
    freelancer_request.delete()

    messages.warning(request, "Freelancer rejected.")
    return redirect('notify')  # Redirige a la página de notificaciones
'''