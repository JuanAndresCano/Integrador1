from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils import timezone
from apps.accounts.models import Client, Freelancer, Project, ProjectContributor, Transaction
from django.contrib.auth.models import User
from decimal import Decimal

class TestConfirmedPayment(TestCase):

    def setUp(self):
        # Configuración de datos de prueba
        self.client_user = User.objects.create_user(username="client", password="pass")
        self.freelancer_user = User.objects.create_user(username="freelancer", password="pass")
        self.client = Client.objects.create(user=self.client_user)
        self.freelancer = Freelancer.objects.create(user=self.freelancer_user)
        self.project = Project.objects.create(title="Test Project", budget=Decimal("1000.00"), client=self.client)
        self.project_contributor = ProjectContributor.objects.create(
            freelancer=self.freelancer,
            project=self.project,
            budget=Decimal("1000.00"),
            finishJob=True
        )
        self.confirmed_payment_url = reverse('confirmedPayment', args=[self.project_contributor.id])

    def test_confirmed_payment_access(self):
        """Test para verificar el acceso a la página de confirmedPayment."""
        self.client.login(username="client", password="pass")
        response = self.client.get(self.confirmed_payment_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "¡Pago Confirmado!")

    def test_successful_transaction_creation(self):
        """Test para verificar que una transacción se crea y el balance del freelancer se actualiza."""
        self.client.login(username="client", password="pass")
        response = self.client.get(self.confirmed_payment_url)

        # Verificar que la transacción fue creada
        transaction = Transaction.objects.filter(
            project_contributor=self.project_contributor,
            client=self.client,
            freelancer=self.freelancer,
            project=self.project,
            amount=self.project_contributor.budget,
            status='completed'
        ).exists()
        self.assertTrue(transaction)

        # Verificar el balance del freelancer
        self.freelancer.refresh_from_db()
        self.assertEqual(self.freelancer.balance, Decimal("1000.00"))

    def test_confirmed_payment_with_unfinished_job(self):
        """Test para verificar que no se permite acceso a confirmedPayment si el trabajo no está terminado."""
        self.project_contributor.finishJob = False
        self.project_contributor.save()
        
        self.client.login(username="client", password="pass")
        response = self.client.get(self.confirmed_payment_url)
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(str(messages[0]), "Payment could not be completed.")
