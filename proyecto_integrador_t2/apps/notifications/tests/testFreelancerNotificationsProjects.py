from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.notifications.models import Notification
from apps.projects.models import Project, ProjectContributor, ProjectComplexity
from apps.accounts.models import Freelancer, Client
from django.contrib import messages

User = get_user_model()

class TestFreelancerNotificationViews(TestCase):
    def setUp(self):
        # Crear usuario cliente y perfil
        self.client_user = User.objects.create_user(username='clientuser', password='password123')
        self.client_profile = Client.objects.create(user=self.client_user, phoneNumber="123456789")
        
        # Crear freelancer y perfil
        self.freelancer_user = User.objects.create_user(username='freelanceruser', password='password123')
        self.freelancer_profile = Freelancer.objects.create(user=self.freelancer_user, phoneNumber="987654321")
        
        # Crear un proyecto y asignarlo al cliente
        complexity = ProjectComplexity.objects.create(levelName="Simple", description="Simple project")
        self.project = Project.objects.create(
            title="Test Project",
            client=self.client_profile,
            complexity=complexity,
            budget=1000
        )
        
        # Crear un ProjectContributor (freelancer) para el proyecto
        self.project_contributor = ProjectContributor.objects.create(
            title="Test Contributor",
            project=self.project,
            freelancer=self.freelancer_profile,
            budget=500,
            version=1,
            is_send=True
        )

    def test_send_request_notification(self):
        # Verificar que cuando el freelancer envía su solicitud, se envía una notificación
        response = self.client.post(reverse('sendRequest', kwargs={'pk': self.project_contributor.pk}))
        
        # Comprobar que la notificación ha sido enviada al cliente
        notification = Notification.objects.filter(destinity=self.client_user, verb__contains="has requested to work on your project").first()
        self.assertIsNotNone(notification)
        self.assertIn(self.project.title, notification.verb)  # Verifica que el título del proyecto esté presente en la notificación
        self.assertEqual(response.status_code, 302)  # Redirección esperada después de enviar la solicitud

    def test_add_milestone_notification(self):
        # Verificar que cuando se añade un entregable y se solicita aprobación, se envía una notificación al cliente
        milestone = self.project_contributor.milestones.create(name="First Milestone")

        deliverable = milestone.deliverables.create(name="Deliverable 1", milestone=milestone)
        
        # Simular la acción de solicitud de aprobación
        response = self.client.post(reverse('deliverablesProject', kwargs={'pk': self.project.pk}), {
            'deliverable_id': deliverable.id,
            'mark_as_completed': 'true'
        })

        # Verificar que la notificación fue enviada al cliente
        notification = Notification.objects.filter(destinity=self.client_user, verb__contains="requested client approval").first()
        self.assertIsNotNone(notification)
        self.assertIn(self.project.title, notification.verb)  # Verifica que el título del proyecto esté presente en la notificación
        self.assertEqual(response.status_code, 302)  # Redirección esperada después de la solicitud

    def test_apply_for_job_notification(self):
        # Verificar que cuando el freelancer aplica a un trabajo, se envía una notificación
        response = self.client.post(reverse('apply_for_job', kwargs={'project_contributor_id': self.project_contributor.pk}))
        
        # Comprobar que la notificación ha sido enviada al cliente
        notification = Notification.objects.filter(destinity=self.client_user, verb__contains="You have successfully applied for this job").first()
        self.assertIsNotNone(notification)
        self.assertIn(self.project.title, notification.verb)  # Verifica que el título del proyecto esté presente en la notificación
        self.assertEqual(response.status_code, 302)  # Redirección esperada después de aplicar

    def test_freelancer_browse_projects(self):
        # Verificar que cuando el freelancer navega por los proyectos, no se crea una notificación
        response = self.client.get(reverse('browseProjects'))
        
        # No esperamos que se haya enviado ninguna notificación
        notifications = Notification.objects.filter(destinity=self.freelancer_user)
        self.assertEqual(notifications.count(), 0)
        self.assertEqual(response.status_code, 200)

    def test_freelancer_browse_own_projects(self):
        # Verificar que cuando el freelancer navega por sus propios proyectos, no se crea una notificación
        response = self.client.get(reverse('browseOwnProjects'))
        
        # No esperamos que se haya enviado ninguna notificación
        notifications = Notification.objects.filter(destinity=self.freelancer_user)
        self.assertEqual(notifications.count(), 0)
        self.assertEqual(response.status_code, 200)
    def test_deliverable_assigned_notification(self):
        # Crear un entregable para el proyecto
        milestone = self.project_contributor.milestones.create(name="First Milestone")
        deliverable = milestone.deliverables.create(name="Deliverable 1", milestone=milestone)
        
        # Asignar el entregable y guardar
        deliverable.is_assigned = True
        deliverable.save()
        
        # Verificar que el cliente recibe una notificación
        notification = Notification.objects.filter(destinity=self.client_user, verb__contains="assigned a deliverable").first()
        self.assertIsNotNone(notification)
        self.assertIn(self.project.title, notification.verb)


