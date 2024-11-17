from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.projects.models import Project, ProjectContributor, Milestone, ProjectComplexity, Deliverable
from apps.accounts.models import Freelancer, Client

User = get_user_model()

class TestDeliverablesFreelancer(TestCase):
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

        # Crear entregables asociados al proyecto
        milestone = Milestone.objects.create(name="Milestone 1", projectContributor=self.project_contributor)
        self.deliverable1 = Deliverable.objects.create(
            name="Deliverable 1",
            description="Description of Deliverable 1",
            deadlineInDays=10,
            requiresEvidence=True,
            milestone=milestone,
            done=False,
            awaiting_approval=True,
            approval_requested=True
        )
        self.deliverable2 = Deliverable.objects.create(
            name="Deliverable 2",
            description="Description of Deliverable 2",
            deadlineInDays=5,
            requiresEvidence=False,
            milestone=milestone,
            done=True,
            awaiting_approval=False,
            approval_requested=False
        )
        self.client.login(username='freelanceruser', password='testpass')

    def test_view_deliverables(self):
        # Obtener la URL de la página de proyectos activos
        url = reverse('browseOwnProjects')  # Cambia esto por la URL correcta
        response = self.client.get(url)

        # Verificar que la página se carga correctamente
        self.assertEqual(response.status_code, 200)

        # Verificar que los entregables estén presentes en la respuesta
        self.assertContains(response, "Deliverable 1")
        self.assertContains(response, "Description of Deliverable 1")
        self.assertContains(response, "10")  # deadlineInDays
        self.assertContains(response, "Not Done")  # 'done' es False

        self.assertContains(response, "Deliverable 2")
        self.assertContains(response, "Description of Deliverable 2")
        self.assertContains(response, "5")  # deadlineInDays
        self.assertContains(response, "Done")  # 'done' es True

        # Verificar que los estados de los entregables son correctos
        self.assertContains(response, "Awaiting Approval")
        self.assertContains(response, "Approval Requested")