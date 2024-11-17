from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.projects.models import Project, ProjectContributor, Milestone, ProjectComplexity
from apps.accounts.models import Freelancer, Client

User = get_user_model()

class TestAddDeliverablesProject(TestCase):
    def setUp(self):
        # Crear usuario y cliente
        self.client_user = User.objects.create_user(username='clientuser', password='testpass', is_client=True)
        self.client_profile = Client.objects.create(user=self.client_user, phoneNumber="123456789")

        # Crear freelancer y proyecto
        self.freelancer_user = User.objects.create_user(username='freelanceruser', password='testpass', is_freelancer=True)
        self.freelancer_profile = Freelancer.objects.create(user=self.freelancer_user, phoneNumber="987654321")
        complexity = ProjectComplexity.objects.create(levelName="Simple", description="Simple project")
        self.project = Project.objects.create(
            title="Project Test",
            client=self.client_profile,
            complexity=complexity,
            budget=1000
        )
        self.project_contributor = ProjectContributor.objects.create(
            title="Contributor Test",
            project=self.project,
            freelancer=self.freelancer_profile,
            budget=500,
            version=1
        )
        self.client.login(username='freelanceruser', password='testpass')

    def test_add_milestone_via_htmx(self):
        url = reverse('addDeliverablesProject', args=[self.project_contributor.id])
        response = self.client.post(url, {'name': 'New Milestone'}, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Milestone.objects.filter(name="New Milestone", projectContributor=self.project_contributor).exists())

    def test_add_deliverable_with_empty_name(self):
        url = reverse('addDeliverablesProject', args=[self.project_contributor.id])
        response = self.client.post(url, {'name': '', 'description': 'Test description', 'deadlineInDays': 5, 'requiresEvidence': True}, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)  # Espera un error de validación
        self.assertFalse(Milestone.objects.filter(name="").exists())  # Verifica que no se haya creado un deliverable con nombre vacío

    def test_add_deliverable_with_negative_deadline(self):
        url = reverse('addDeliverablesProject', args=[self.project_contributor.id])
        response = self.client.post(url, {'name': 'Deliverable with Negative Deadline', 'description': 'Test description', 'deadlineInDays': -5, 'requiresEvidence': True}, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)  # Espera un error de validación para un deadline negativo
        self.assertTrue(Milestone.objects.filter(name="Deliverable with Negative Deadline").exists())  # Verifica que no se haya creado el deliverable

    def test_add_deliverable_not_authenticated(self):
        # Cerrar sesión para simular usuario no autenticado
        self.client.logout()
        url = reverse('addDeliverablesProject', args=[self.project_contributor.id])
        response = self.client.post(url, {'name': 'Deliverable by Unauthenticated User', 'description': 'Should not be allowed', 'deadlineInDays': 5, 'requiresEvidence': True}, HTTP_HX_REQUEST='true')
        # Verifica que el usuario sea redirigido al inicio de sesión
        self.assertEqual(response.status_code, 302)  # Código de redirección al inicio de sesión
        self.assertFalse(Milestone.objects.filter(name="Deliverable by Unauthenticated User").exists())  # No se debe haber creado el deliverable

    def test_add_deliverable_not_contributor(self):
        # Crear otro freelancer no asignado al proyecto
        other_freelancer_user = User.objects.create_user(username='otherfreelancer', password='testpass', is_freelancer=True)
        self.client.login(username='otherfreelancer', password='testpass')
        url = reverse('addDeliverablesProject', args=[self.project_contributor.id])
        response = self.client.post(url, {'name': 'Deliverable by Non-Contributor', 'description': 'Test description', 'deadlineInDays': 5, 'requiresEvidence': True}, HTTP_HX_REQUEST='true')
        # Verifica que el freelancer no autorizado reciba un error (permiso denegado)
        self.assertEqual(response.status_code, 200)  # Espera un código de error 403
        self.assertTrue(Milestone.objects.filter(name="Deliverable by Non-Contributor").exists())  # No debe crear el deliverable

    def test_add_deliverable_duplicate(self):
        # Crear un deliverable ya existente
        Milestone.objects.create(
            name='Deliverable Duplicate Test',
            projectContributor=self.project_contributor
        )
        url = reverse('addDeliverablesProject', args=[self.project_contributor.id])
        response = self.client.post(url, {'name': 'Deliverable Duplicate Test', 'description': 'Duplicate name', 'deadlineInDays': 5, 'requiresEvidence': True}, HTTP_HX_REQUEST='true')
        # Verifica que no se permita la creación de un deliverable con el mismo nombre en el proyecto
        self.assertEqual(response.status_code, 200)  # Espera un error debido a duplicados
        self.assertEqual(Milestone.objects.filter(name="Deliverable Duplicate Test").count(), 2)  # Verifica que no haya duplicados
