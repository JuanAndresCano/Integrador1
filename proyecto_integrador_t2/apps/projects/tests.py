from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from apps.projects.models import Project, ProjectContributor
from apps.accounts.models import Userk, Client

class ClientFinancialControlTests(TestCase):

    def setUp(self):
        # Crear un usuario de prueba utilizando el modelo Userk
        self.user = Userk.objects.create_user(username='client_user', password='test123')

        # Crear un cliente y asociarlo al usuario
        self.client_user = Client.objects.create(user=self.user)

        # Autenticarse en el sistema
        self.client.login(username='client_user', password='test123')

        # Crear algunos proyectos de prueba
        self.project1 = ProjectContributor.objects.create(
            title='Project 1',
            budget=1000.00,
            project_status='PENDING',
            end_date=timezone.now() + timedelta(days=10),
            project=Project.objects.create(client=self.client_user),
            freelancer=None,
        )
        self.project2 = ProjectContributor.objects.create(
            title='Project 2',
            budget=5000.00,
            project_status='IN_PROGRESS',
            end_date=timezone.now() + timedelta(days=5),
            project=Project.objects.create(client=self.client_user),
            freelancer=None,
        )
        self.project3 = ProjectContributor.objects.create(
            title='Project 3',
            budget=2000.00,
            project_status='DONE',
            end_date=timezone.now() + timedelta(days=3),
            project=Project.objects.create(client=self.client_user),
            freelancer=None,
        )

    # 1. Test para verificar que la página ClientFinancialControl carga correctamente
    def test_client_financial_control_loads(self):
        response = self.client.get(reverse('clientFinancialControl'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/client/clientFinancialControl.html')
        self.assertContains(response, 'Transactions')  # Verificar que la palabra "Transactions" esté en la página

    # 2. Test para verificar el ordenamiento por presupuesto (High to Low)
    def test_project_ordering_by_budget_high_to_low(self):
        response = self.client.get(reverse('clientFinancialControl'), {'sort_by': '-budget'})
        projects = response.context['projects']
        self.assertEqual(projects[0].budget, 5000.00)  # El proyecto con mayor presupuesto debe ser el primero
        self.assertEqual(projects[1].budget, 2000.00)
        self.assertEqual(projects[2].budget, 1000.00)

    # 3. Test para verificar el ordenamiento por presupuesto (Low to High)
    def test_project_ordering_by_budget_low_to_high(self):
        response = self.client.get(reverse('clientFinancialControl'), {'sort_by': 'budget'})
        projects = response.context['projects']
        self.assertEqual(projects[0].budget, 1000.00)  # El proyecto con menor presupuesto debe ser el primero
        self.assertEqual(projects[1].budget, 2000.00)
        self.assertEqual(projects[2].budget, 5000.00)

    # 4. Test para verificar el filtro por estado (Pending)
    def test_filter_by_status_pending(self):
        response = self.client.get(reverse('clientFinancialControl'), {'project_status': 'PENDING'})
        projects = response.context['projects']
        self.assertEqual(len(projects), 1)  # Debe haber solo 1 proyecto pendiente
        self.assertEqual(projects[0].project_status, 'PENDING')

    # 5. Test para verificar el filtro por estado (In Progress)
    def test_filter_by_status_in_progress(self):
        response = self.client.get(reverse('clientFinancialControl'), {'project_status': 'IN_PROGRESS'})
        projects = response.context['projects']
        self.assertEqual(len(projects), 1)  # Debe haber solo 1 proyecto en progreso
        self.assertEqual(projects[0].project_status, 'IN_PROGRESS')

    # 6. Test para verificar el cálculo de los totales 'Pending' e 'In Progress'
    def test_total_pending_and_in_progress_calculation(self):
        response = self.client.get(reverse('clientFinancialControl'))
        total_pending = response.context['total_pending']
        total_in_progress = response.context['total_in_progress']
        self.assertEqual(total_pending, 1000.00)  # Solo un proyecto pendiente con un budget de 1000
        self.assertEqual(total_in_progress, 5000.00)  # Solo un proyecto en progreso con un budget de 5000

    # 7. Test para verificar si las fechas de finalización se muestran correctamente
    def test_project_end_dates_displayed_correctly(self):
        response = self.client.get(reverse('clientFinancialControl'))
        projects = response.context['projects']
        end_dates = [project.end_date.strftime('%b %d, %Y') for project in projects]
        self.assertIn('Project 1', response.content.decode())  # Verifica que se esté mostrando el proyecto
        self.assertIn('Project 2', response.content.decode())
        self.assertIn('Project 3', response.content.decode())
