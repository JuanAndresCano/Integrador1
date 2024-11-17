from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.notifications.models import Notification
from apps.projects.models import Project, ProjectContributor, ProjectComplexity
from apps.accounts.models import Freelancer, Client

User = get_user_model()

class testClientNotificationprojects(TestCase):
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

    def test_project_creation_notification(self):
        # Verificar que al crear un proyecto, el cliente recibe una notificación
        notification = Notification.objects.filter(destinity=self.client_user, verb__contains="created the project").first()
        self.assertIsNotNone(notification)

    def test_freelancer_application_notification(self):
        # Verificar que al enviar una solicitud, el cliente reciba una notificación
        self.project_contributor.approval_status = "pending"
        self.project_contributor.rejectionReason = "pending"
        self.project_contributor.save()
        
        notification = Notification.objects.filter(destinity=self.client_user, verb__contains="has requested to work on your project").first()
        self.assertIsNotNone(notification)
        # Verificar que el título del proyecto esté en la notificación
        self.assertIn(self.project.title, notification.verb)  # Verifica que el título del proyecto esté presente en el mensaje

    def test_client_acceptance_notification(self):
        # Verificar que cuando el cliente acepta una solicitud, el freelancer recibe una notificación
        self.project_contributor.approval_status = "not_rejected"
        self.project_contributor.rejectionReason = "not_rejected"
        self.project_contributor.save()
        
        notification = Notification.objects.filter(destinity=self.freelancer_user, verb__contains="accepted your proposal").first()
        self.assertIsNotNone(notification)
        self.assertIn(self.project_contributor.title, notification.verb)  # Usar contributor title en lugar de project title

    def test_client_rejection_notification(self):
        # Verificar que cuando el cliente rechaza una solicitud, el freelancer recibe una notificación
        self.project_contributor.rejectionReason = "profile_rejected"
        self.project_contributor.save()
        
        notification = Notification.objects.filter(destinity=self.freelancer_user, verb__contains="rejected your proposal").first()
        self.assertIsNotNone(notification)
        self.assertIn(self.project_contributor.title, notification.verb)  # Usar contributor title en lugar de project title

    def test_freelancer_submission_notification(self):
        # Verificar que cuando el freelancer envía su propuesta, el cliente recibe una notificación
        self.project_contributor.approval_status = "not_rejected"
        self.project_contributor.rejectionReason = "not_rejected"
        self.project_contributor.is_send = True
        self.project_contributor.save()
        
        notification = Notification.objects.filter(destinity=self.client_user, verb__contains="has submitted their proposal").first()
        self.assertIsNotNone(notification)
        # Verificar que el título del proyecto esté en la notificación
        self.assertIn(self.project.title, notification.verb)

        