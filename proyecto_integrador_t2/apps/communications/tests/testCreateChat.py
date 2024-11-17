from django.test import TestCase, Client as TestClient  # Importa TestClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from apps.accounts.models import *
from apps.communications.models import *

class TestCreateChat(TestCase):

    def setUp(self):
        self.testClient = TestClient()
        self.clientUser = Userk.objects.create_user(username='clientUser', password='testPassword', is_client=True)
        self.freelancerUser = Userk.objects.create_user(username='freelancerUser', password='testPassword', is_freelancer=True)
        
        # Instancias de Client y Freelancer
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
        
        # Crear chat inicial
        self.chat = Chat.objects.create(
            chatName='testChat',
            freelancer=self.freelancer,
            client=self.testClientInstance
        )
        
        self.freelancerCreateChatUrl = reverse('freelancerCreateComprobateChat', args=[self.clientUser.username])
        self.clientCreateChatUrl = reverse('clientCreateComprobateChat', args=[self.freelancerUser.username])

    def testCreateNewChatForClient(self):
        """Prueba que el cliente cree un nuevo chat con un freelancer si no existe"""
        # Iniciar sesión como cliente
        self.testClient.login(username='clientUser', password='testPassword')
        
        # Realizar solicitud para crear un chat
        response = self.testClient.get(self.clientCreateChatUrl)
        
        # Verificar existencia de chat y redirección
        chat = Chat.objects.filter(client=self.testClientInstance, freelancer=self.freelancer).first()
        self.assertIsNotNone(chat)
        self.assertRedirects(response, reverse('clientMessage', args=[chat.chatName]))

    def testRedirectToExistingChatForClient(self):
        """Prueba que el cliente sea redirigido a un chat existente sin crear uno nuevo"""
        # Asegurarse de que el chat exista
        existingChat = Chat.objects.filter(client=self.testClientInstance, freelancer=self.freelancer).first()
        
        # Iniciar sesión como cliente
        self.testClient.login(username='clientUser', password='testPassword')
        
        # Solicitar redirección al chat existente
        response = self.testClient.get(self.clientCreateChatUrl)
        
        # Confirmar que solo existe un chat
        self.assertEqual(Chat.objects.filter(client=self.testClientInstance, freelancer=self.freelancer).count(), 1)
        self.assertRedirects(response, reverse('clientMessage', args=[existingChat.chatName]))

    def testCreateNewChatForFreelancer(self):
        """Prueba que el freelancer cree un nuevo chat con un cliente si no existe"""
        # Iniciar sesión como freelancer
        self.testClient.login(username='freelancerUser', password='testPassword')
        
        # Realizar solicitud para crear un chat
        response = self.testClient.get(self.freelancerCreateChatUrl)
        
        # Verificar existencia de chat y redirección
        chat = Chat.objects.filter(client=self.testClientInstance, freelancer=self.freelancer).first()
        self.assertIsNotNone(chat)
        self.assertRedirects(response, reverse('freelancerMessage', args=[chat.chatName]))

    def testRedirectToExistingChatForFreelancer(self):
        """Prueba que el freelancer sea redirigido a un chat existente sin crear uno nuevo"""
        # Asegurarse de que el chat exista
        existingChat = Chat.objects.filter(client=self.testClientInstance, freelancer=self.freelancer).first()
        
        # Iniciar sesión como freelancer
        self.testClient.login(username='freelancerUser', password='testPassword')
        
        # Solicitar redirección al chat existente
        response = self.testClient.get(self.freelancerCreateChatUrl)
        
        # Confirmar que solo existe un chat
        self.assertEqual(Chat.objects.filter(client=self.testClientInstance, freelancer=self.freelancer).count(), 1)
        self.assertRedirects(response, reverse('freelancerMessage', args=[existingChat.chatName]))
