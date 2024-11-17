from django.test import TestCase, Client as TestClient  # Importa TestClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from apps.accounts.models import *
from apps.notifications.models import *

class TestSecurity(TestCase):

    def setUp(self):
        self.testClient = TestClient()  # Se utiliza para hacer peticiones HTTP
        # Crear usuarios 'clientUser' y 'freelancerUser' para las pruebas
        self.clientUser = Userk.objects.create_user(username='clientUser', password='testpassword', is_client=True)
        self.freelancerUser = Userk.objects.create_user(username='freelancerUser', password='testpassword', is_freelancer=True)

        # Crear instancias de Client y Freelancer asociadas a los usuarios
        self.testClientInstance = Client.objects.create(  # Cambié el nombre aquí
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

    def testClientAccessToNotifications(self):
        # Autenticarse como un usuario 'client'
        self.testClient.login(username='clientUser', password='testpassword')  # Usando self.testClient

        # Acceder a la vista 'clientMessageHome'
        response = self.testClient.get(reverse('notifications'))  # Usando self.testClient

        # Comprobar que la respuesta es 200 (acceso permitido)
        self.assertEqual(response.status_code, 200)

    def testFreelancerAccessToNotifications(self):
        # Autenticarse como un usuario 'freelancer'
        self.testClient.login(username='freelancerUser', password='testpassword')  # Usando self.testClient

        # Intentar acceder a la vista 'clientMessageHome'
        response = self.testClient.get(reverse('notifications'))  # Usando self.testClient
        self.assertEqual(response.status_code, 200)