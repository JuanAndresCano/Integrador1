from apps.projects.models import Deliverable, Project, ProjectContributor, Milestone, ProjectComplexity
from apps.accounts.models import Freelancer, Client, Userk
from django.test import TestCase
from django.urls import reverse

class TestAddMilestoneDeliverable(TestCase):
    def setUp(self):
        # Crear usuario y cliente
        self.client_user = Userk.objects.create_user(username='clientuser', password='testpass', is_client=True)
        self.client_profile = Client.objects.create(user=self.client_user, phoneNumber="123456789")

        # Crear freelancer y proyecto
        self.freelancer_user = Userk.objects.create_user(username='freelanceruser', password='testpass', is_freelancer=True)
        self.freelancer_profile = Freelancer.objects.create(user=self.freelancer_user, phoneNumber="987654321")

        # Crear complejidad del proyecto
        complexity = ProjectComplexity.objects.create(levelName="Simple", description="Simple project")

        # Crear proyecto y contributor
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

        # Iniciar sesión como freelancer
        self.client.login(username='freelanceruser', password='testpass')

        # Crear Milestone
        self.milestone = Milestone.objects.create(name="Milestone Test", projectContributor=self.project_contributor)

    def test_add_deliverable(self):
        url = reverse('addMilestoneDeliverable', args=[self.milestone.id])
        response = self.client.post(url, {
            'name': 'New Deliverable',
            'description': 'Description',
            'deadlineInDays': 5,
            'requiresEvidence': True
        })
        self.assertEqual(response.status_code, 302)  # Redirect to next step
        self.assertTrue(Deliverable.objects.filter(name="New Deliverable", milestone=self.milestone).exists())

    def test_add_deliverable_not_authenticated(self):
        # Cerrar sesión
        self.client.logout()
        url = reverse('addMilestoneDeliverable', args=[self.milestone.id])
        response = self.client.post(url, {
            'name': 'Deliverable Unauthenticated',
            'description': 'Should not be added',
            'deadlineInDays': 3,
            'requiresEvidence': True
        })
        # Verifica que el usuario sea redirigido a la página de inicio de sesión
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Deliverable.objects.filter(name="Deliverable Unauthenticated").exists())

    def test_add_deliverable_without_permission(self):
        # Crear un usuario diferente
        other_user = Userk.objects.create_user(username='otheruser', password='testpass', is_freelancer=True)
        self.client.login(username='otheruser', password='testpass')
        url = reverse('addMilestoneDeliverable', args=[self.milestone.id])
        response = self.client.post(url, {
            'name': 'Unauthorized Deliverable',
            'description': 'Should not be added',
            'deadlineInDays': 3,
            'requiresEvidence': True
        })
        # Verifica que el usuario reciba un código de error de permiso denegado
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Deliverable.objects.filter(name="Unauthorized Deliverable").exists())

    def test_add_deliverable_without_name(self):
        url = reverse('addMilestoneDeliverable', args=[self.milestone.id])
        response = self.client.post(url, {
            'name': '',
            'description': 'No name provided',
            'deadlineInDays': 4,
            'requiresEvidence': False
        })
        # Verifica que el campo de nombre es obligatorio y causa un error
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Deliverable.objects.filter(description="No name provided").exists())

    def test_add_deliverable_with_negative_deadline(self):
        url = reverse('addMilestoneDeliverable', args=[self.milestone.id])
        response = self.client.post(url, {
            'name': 'Negative Deadline Deliverable',
            'description': 'Invalid deadline',
            'deadlineInDays': -5,
            'requiresEvidence': True
        })
        # Verifica que un deadline negativo no es permitido
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Deliverable.objects.filter(name="Negative Deadline Deliverable").exists())

    def test_add_duplicate_deliverable(self):
        # Añadir el primer deliverable
        Deliverable.objects.create(
            name="Duplicate Deliverable",
            description="First instance",
            deadlineInDays=7,
            requiresEvidence=True,
            milestone=self.milestone
        )
        # Intentar añadir un deliverable duplicado
        url = reverse('addMilestoneDeliverable', args=[self.milestone.id])
        response = self.client.post(url, {
            'name': 'Duplicate Deliverable',
            'description': 'Duplicate instance',
            'deadlineInDays': 7,
            'requiresEvidence': True
        })
        # Verifica que no permite añadir un deliverable con el mismo nombre y milestone
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Deliverable.objects.filter(name="Duplicate Deliverable").count(), 1)
