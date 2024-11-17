from django.test import TestCase, Client as TestClient  # Importa TestClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from apps.accounts.models import *
from apps.communications.models import *

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
        
        # Crear un chat de prueba entre el freelancer y el client
        self.chat = Chat.objects.create(
            chatName='testChat',
            freelancer=self.freelancer,
            client=self.testClientInstance  # Cambié el nombre aquí también
        )

    def testClientAccessToClientMessageHome(self):
        # Autenticarse como un usuario 'client'
        self.testClient.login(username='clientUser', password='testpassword')  # Usando self.testClient

        # Acceder a la vista 'clientMessageHome'
        response = self.testClient.get(reverse('clientMessageHome'))  # Usando self.testClient

        # Comprobar que la respuesta es 200 (acceso permitido)
        self.assertEqual(response.status_code, 200)

    def testFreelancerAccessToClientMessageHome(self):
        # Autenticarse como un usuario 'freelancer'
        self.testClient.login(username='freelancerUser', password='testpassword')  # Usando self.testClient

        # Intentar acceder a la vista 'clientMessageHome'
        response = self.testClient.get(reverse('clientMessageHome'))  # Usando self.testClient

        self.assertContains(response, 'You are not God to view this page bro')
        self.assertEqual(response.status_code, 200)

    def testUnauthenticatedUserAccessToClientMessageHome(self):
        # Intentar acceder sin autenticarse
        response = self.testClient.get(reverse('clientMessageHome'))  # Usando self.testClient

        # Comprobar que la respuesta es 302 (redirección al login)
        self.assertRedirects(response, '/login/?next=/clientMessageHome/')
        self.assertEqual(response.status_code, 302)

    def testFreelancerAccessToFreelancerMessageHome(self):
        # Autenticarse como un usuario 'freelancer'
        self.testClient.login(username='freelancerUser', password='testpassword')  # Usando self.testClient

        # Acceder a la vista 'freelancerMessageHome'
        response = self.testClient.get(reverse('freelancerMessageHome'))  # Usando self.testClient

        # Comprobar que la respuesta es 200 (acceso permitido)
        self.assertEqual(response.status_code, 200)

    def testClientAccessToFreelancerMessageHome(self):
        # Autenticarse como un usuario 'client'
        self.testClient.login(username='clientUser', password='testpassword')  # Usando self.testClient

        # Intentar acceder a la vista 'freelancerMessageHome'
        response = self.testClient.get(reverse('freelancerMessageHome'))  # Usando self.testClient

        self.assertContains(response, 'You are not God to view this page bro')
        self.assertEqual(response.status_code, 200)

    def testUnauthenticatedUserAccessToFreelancerMessageHome(self):
        # Intentar acceder sin autenticarse
        response = self.testClient.get(reverse('freelancerMessageHome'))  # Usando self.testClient

        # Comprobar que la respuesta es 302 (redirección al login)
        self.assertRedirects(response, '/login/?next=/freelancerMessageHome/')
        self.assertEqual(response.status_code, 302)

    def testAccessToMessageClientViewAsClient(self):
        # Autenticarse como 'client'
        self.testClient.login(username='clientUser', password='testpassword')  # Usando self.testClient

        # Acceder a un chat de cliente
        response = self.testClient.get(reverse('clientMessage', args=[self.chat.chatName]))  # Usando self.testClient

        # Comprobar que la respuesta es 200 (acceso permitido)
        self.assertEqual(response.status_code, 200)

    def testAccessToMessageClientViewAsFreelancer(self):
        # Autenticarse como un usuario 'client'
        self.testClient.login(username='freelancerUser', password='testpassword')  # Usando self.testClient

        # Intentar acceder a la vista 'freelancerMessageHome'
        response = self.testClient.get(reverse('clientMessage', args=[self.chat.chatName]))  # Usando self.testClient

        self.assertContains(response, 'You are not God to view this page bro')
        self.assertEqual(response.status_code, 200)

    def testAccessToMessageClientViewAsUnauthenticated(self):
        # Intentar acceder sin autenticarse
        response = self.testClient.get(reverse('clientMessage', args=[self.chat.chatName]))  # Usando self.testClient

        # Comprobar que la respuesta es 302 (redirección al login)
        expected_url = f'/login/?next=/clientMessage/{self.chat.chatName}'
        self.assertRedirects(response, expected_url)
        self.assertEqual(response.status_code, 302)

    def testAccessToMessageFreelancerViewAsFreelancer(self):
        # Autenticarse como 'freelancer'
        self.testClient.login(username='freelancerUser', password='testpassword')  # Usando self.testClient

        # Acceder a un chat de freelancer
        response = self.testClient.get(reverse('freelancerMessage', args=[self.chat.chatName]))  # Usando self.testClient

        # Comprobar que la respuesta es 200 (acceso permitido)
        self.assertEqual(response.status_code, 200)

    def testAccessToMessageFreelancerViewAsFreelancer(self):
        # Autenticarse como un usuario 'client'
        self.testClient.login(username='clientUser', password='testpassword')  # Usando self.testClient

        # Intentar acceder a la vista 'freelancerMessageHome'
        response = self.testClient.get(reverse('freelancerMessage', args=[self.chat.chatName]))  # Usando self.testClient

        self.assertContains(response, 'You are not God to view this page bro')
        self.assertEqual(response.status_code, 200)
        

    def testAccessToMessageFreelancerViewAsUnauthenticated(self):
        # Intentar acceder sin autenticarse
        response = self.testClient.get(reverse('freelancerMessage', args=[self.chat.chatName]))  # Usando self.testClient

        # Comprobar que la respuesta es 302 (redirección al login)
        expected_url = f'/login/?next=/freelancerMessage/{self.chat.chatName}'
        self.assertRedirects(response, expected_url)
        self.assertEqual(response.status_code, 302)

    #-----------------------------------------------------------------------------------

    def testAccessToClientCreateComprobateChatAsFreelancer(self):
        # Autenticarse como 'freelancer'
        self.testClient.login(username='freelancerUser', password='testpassword')  # Usando self.testClient

        # Acceder a la vista 'clientCreateComprobateChat' con un nombre de usuario
        response = self.testClient.get(reverse('clientCreateComprobateChat', args=[self.clientUser.username]))  # Usando self.testClient

        # Comprobar que la respuesta es 200 (acceso permitido)
        self.assertContains(response, 'You are not God to view this page bro')
        self.assertEqual(response.status_code, 200)

    def testAccessToFreelancerCreateComprobateChatAsClient(self):
        # Autenticarse como 'client'
        self.testClient.login(username='clientUser', password='testpassword')  # Usando self.testClient

        # Acceder a la vista 'freelancerCreateComprobateChat' con un nombre de usuario
        response = self.testClient.get(reverse('freelancerCreateComprobateChat', args=[self.freelancerUser.username]))  # Usando self.testClient

        # Comprobar que la respuesta es 200 (acceso permitido)
        self.assertContains(response, 'You are not God to view this page bro')
        self.assertEqual(response.status_code, 200)

    def testAccessToClientCreateComprobateChatAsUnauthenticated(self):
        # Intentar acceder sin autenticarse
        response = self.testClient.get(reverse('clientCreateComprobateChat', args=[self.clientUser.username]))  # Usando self.testClient

        # Comprobar que la respuesta es 302 (redirección al login)
        expected_url = f'/login/?next=/clientCreateComprobateChat/{self.clientUser.username}'
        self.assertRedirects(response, expected_url)
        self.assertEqual(response.status_code, 302)

    def testAccessToFreelancerCreateComprobateChatAsUnauthenticated(self):
        # Intentar acceder sin autenticarse
        response = self.testClient.get(reverse('freelancerCreateComprobateChat', args=[self.freelancerUser.username]))  # Usando self.testClient

        # Comprobar que la respuesta es 302 (redirección al login)
        expected_url = f'/login/?next=/freelancerCreateComprobateChat/{self.freelancerUser.username}'
        self.assertRedirects(response, expected_url)
        self.assertEqual(response.status_code, 302)

    def testAccessToClientCreateComprobateChatAsClient(self):
        # Autenticarse como 'client'
        self.testClient.login(username='clientUser', password='testpassword')  # Usando self.testClient

        # Acceder a la vista 'clientCreateComprobateChat' con un nombre de usuario
        response = self.testClient.get(reverse('clientCreateComprobateChat', args=[self.freelancerUser.username]))  # Usando self.testClient

        # Comprobar que la respuesta es 200 (acceso permitido)
        self.assertEqual(response.status_code, 302)

    def testAccessToFreelancerCreateComprobateChatAsFreelancer(self):
        # Autenticarse como 'client'
        self.testClient.login(username='freelancerUser', password='testpassword')  # Usando self.testClient

        # Acceder a la vista 'clientCreateComprobateChat' con un nombre de usuario
        response = self.testClient.get(reverse('freelancerCreateComprobateChat', args=[self.clientUser.username]))  # Usando self.testClient

        # Comprobar que la respuesta es 200 (acceso permitido)
        self.assertEqual(response.status_code, 302)


    
