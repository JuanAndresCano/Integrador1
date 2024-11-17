from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils import timezone
from apps.accounts.models import Client, Freelancer, Project, ProjectContributor, Transaction
from django.contrib.auth.models import User
from decimal import Decimal

class TestGateWay(TestCase):

    def setUp(self):
        # Configurar datos de prueba
        self.client_user = User.objects.create_user(username="client", password="pass")
        self.freelancer_user = User.objects.create_user(username="freelancer", password="pass")
        self.client = Client.objects.create(user=self.client_user)
        self.freelancer = Freelancer.objects.create(user=self.freelancer_user)
        self.project = Project.objects.create(title="Test Project", budget=Decimal("1000.00"), client=self.client)
        self.project_contributor = ProjectContributor.objects.create(
            freelancer=self.freelancer, 
            project=self.project, 
            budget=Decimal("1000.00"), 
            finishJob=True  # Trabajo terminado
        )
        self.gateWay_url = reverse('gateWay', args=[self.project_contributor.id])

    def test_gateWay_access(self):
        """Test para verificar el acceso a la página de gateWay."""
        self.client.login(username="client", password="pass")
        response = self.client.get(self.gateWay_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Realizar Pago")

    def test_successful_payment_redirects_to_confirmed_payment(self):
        """Test de caso exitoso de pago."""
        self.client.login(username="client", password="pass")
        response = self.client.post(self.gateWay_url, {
            'card_number': '1234567890123456',
            'expiry_date': '12/34',
            'cvv': '123',
            'card_name': 'Juan Pérez'
        })
        self.assertRedirects(response, reverse('confirmedPayment', args=[self.project_contributor.id]))

    def test_payment_without_finishJob_redirects_back(self):
        """Test de redirección cuando el trabajo no está terminado."""
        self.project_contributor.finishJob = False
        self.project_contributor.save()
        
        self.client.login(username="client", password="pass")
        response = self.client.get(self.gateWay_url)
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(str(messages[0]), "Payment not allowed until the job is marked as complete.")

    def test_payment_with_missing_fields(self):
        """Test de error en formulario con campos incompletos."""
        self.client.login(username="client", password="pass")
        response = self.client.post(self.gateWay_url, {
            'card_number': '',
            'expiry_date': '12/34',
            'cvv': '',
            'card_name': ''
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(str(messages[0]), "All the fields are required.")
