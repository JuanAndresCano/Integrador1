from django.test import TestCase, Client as TestClient  # Importa TestClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from apps.accounts.models import *
from apps.communications.models import *

class TestMessageHome(TestCase):

    def setUp(self):
        self.testClient = TestClient()
        self.clientUser = Userk.objects.create_user(username='clientUser', password='testpassword', is_client=True)
        self.freelancerUser = Userk.objects.create_user(username='freelancerUser', password='testpassword', is_freelancer=True)
        
        # Client and Freelancer instances
        self.testClientInstance = Client.objects.create(
            user=self.clientUser,
            phoneNumber='123456789',
            taxId='1234567890',
            companyName='TestCompany',
            typeOfCompany='Software',
            businessVertical='IT',
            countryOfLocation='Colombia',
            city='Bogotá',
            address='Av. El Dorado',
        )
        
        self.freelancer = Freelancer.objects.create(
            user=self.freelancerUser,
            phoneNumber='987654321',
            identification='0987654321',
            email='freelancer@example.com',
        )
        
        # Create initial chat
        self.chat = Chat.objects.create(
            chatName='testChat',
            freelancer=self.freelancer,
            client=self.testClientInstance
        )

    def test_client_message_home_view(self):
        """Prueba que el cliente pueda ver la lista de chats y que el chat más reciente se muestre en primer lugar."""
        # Iniciar sesión como cliente
        self.testClient.login(username='clientUser', password='testpassword')

        # Acceder a la vista de clientMessageHome
        response = self.testClient.get(reverse('clientMessageHome'))

        # Verificar que la respuesta es 200 y contiene los datos correctos
        self.assertEqual(response.status_code, 200)
        self.assertIn('chats', response.context)
        self.assertIn('latestChat', response.context)
        self.assertEqual(response.context['latestChat'], self.chat)

    def test_freelancer_message_home_view(self):
        """Prueba que el freelancer pueda ver la lista de chats y que el chat más reciente se muestre en primer lugar."""
        # Iniciar sesión como freelancer
        self.testClient.login(username='freelancerUser', password='testpassword')

        # Acceder a la vista de freelancerMessageHome
        response = self.testClient.get(reverse('freelancerMessageHome'))

        # Verificar que la respuesta es 200 y contiene los datos correctos
        self.assertEqual(response.status_code, 200)
        self.assertIn('chats', response.context)
        self.assertIn('latestChat', response.context)
        self.assertEqual(response.context['latestChat'], self.chat)