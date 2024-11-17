from django.test import TestCase, Client as TestClient
from django.urls import reverse
from apps.accounts.models import Userk, Client, Freelancer
from apps.communications.models import Chat, Message
from apps.communications.forms import ChatMessageCreateForm

class TestMessageViews(TestCase):

    def setUp(self):
        # Inicializa el cliente de prueba
        self.testClient = TestClient()

        # Crear usuarios y sus perfiles asociados
        self.clientUser = Userk.objects.create_user(username='clientUser', password='testpassword', is_client=True)
        self.freelancerUser = Userk.objects.create_user(username='freelancerUser', password='testpassword', is_freelancer=True)

        # Instancias de Client y Freelancer
        self.clientInstance = Client.objects.create(
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

        # Crear un chat entre el cliente y el freelancer con mensajes
        self.chat = Chat.objects.create(chatName='testChat', freelancer=self.freelancer, client=self.clientInstance)
        self.message1 = Message.objects.create(chat=self.chat, author=self.clientUser, body="the prex")
        self.message2 = Message.objects.create(chat=self.chat, author=self.freelancerUser, body="the message")

    def testClientMessageView(self):
        """Prueba que el cliente vea los mensajes de un chat y el formulario de creación de mensajes"""

        # Iniciar sesión como cliente
        self.testClient.login(username='clientUser', password='testpassword')

        # Acceder a la vista de clientMessage
        response = self.testClient.get(reverse('clientMessage', args=['testChat']))

        # Verificar que la respuesta es 200
        self.assertEqual(response.status_code, 200)

        # Verificar que el chat y los mensajes están en el contexto
        self.assertIn('chat', response.context)
        self.assertEqual(response.context['chat'], self.chat)
        self.assertIn('chatMessages', response.context)
        self.assertEqual(len(response.context['chatMessages']), 2)  # Verificar que hay 2 mensajes

        # Verificar que el formulario también está en el contexto
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], ChatMessageCreateForm)

    def testFreelancerMessageView(self):
        """Prueba que el freelancer vea los mensajes de un chat y el formulario de creación de mensajes"""

        # Iniciar sesión como freelancer
        self.testClient.login(username='freelancerUser', password='testpassword')

        # Acceder a la vista de freelancerMessage
        response = self.testClient.get(reverse('freelancerMessage', args=['testChat']))

        # Verificar que la respuesta es 200
        self.assertEqual(response.status_code, 200)

        # Verificar que el chat y los mensajes están en el contexto
        self.assertIn('chat', response.context)
        self.assertEqual(response.context['chat'], self.chat)
        self.assertIn('chatMessages', response.context)
        self.assertEqual(len(response.context['chatMessages']), 2)  # Verificar que hay 2 mensajes

        # Verificar que el formulario también está en el contexto
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], ChatMessageCreateForm)

    def testCreateMessageInClientMessage(self):
        """Prueba que el cliente pueda crear un mensaje y este se guarde correctamente"""

        # Iniciar sesión como cliente
        self.testClient.login(username='clientUser', password='testpassword')

        # Enviar un mensaje en el chat
        messageData = {'body': 'the prex'}
        response = self.testClient.post(reverse('clientMessage', args=['testChat']), messageData)

        # Verificar que el mensaje se haya guardado
        self.assertEqual(Message.objects.count(), 2)  # Debería haber ahora 2 mensajes

        # Verificar que el último mensaje es el que acabamos de enviar
        newMessage = Message.objects.filter(chat=self.chat, author=self.clientUser).order_by('timeCreated').first()
        self.assertEqual(newMessage.body, 'the prex')  # Verificar que el cuerpo es el esperado

        self.assertEqual(newMessage.author, self.clientUser)

    def testCreateMessageInFreelancerMessage(self):
        """Prueba que el freelancer pueda crear un mensaje y este se guarde correctamente"""

        # Iniciar sesión como freelancer
        self.testClient.login(username='freelancerUser', password='testpassword')

        # Enviar un mensaje en el chat
        messageData = {'body': 'the message'}
        response = self.testClient.post(reverse('freelancerMessage', args=['testChat']), messageData)

        # Verificar que el mensaje se haya guardado
        self.assertEqual(Message.objects.count(), 2)  # Debería haber ahora 2 mensajes

        # Verificar que el último mensaje es el que acabamos de enviar
        newMessage = Message.objects.filter(chat=self.chat, author=self.freelancerUser).order_by('timeCreated').first()
        self.assertEqual(newMessage.body, 'the message')  # Verificar que el cuerpo es el esperado

        self.assertEqual(newMessage.author, self.freelancerUser)

    def testMessageClientFormInTemplate(self):
        """Verifica que el formulario de mensaje esté presente en la página"""
        self.testClient.login(username='clientUser', password='testpassword')
        response = self.testClient.get(reverse('clientMessage', args=['testChat']))
        self.assertContains(response, '<form')  # Verifica que haya un formulario en la respuesta
        self.assertContains(response, 'name="body"')  # Verifica que haya un campo para el mensaje

    def testMessageFreelancerFormInTemplate(self):
        """Verifica que el formulario de mensaje esté presente en la página"""
        self.testClient.login(username='freelancerUser', password='testpassword')
        response = self.testClient.get(reverse('freelancerMessage', args=['testChat']))
        self.assertContains(response, '<form')  # Verifica que haya un formulario en la respuesta
        self.assertContains(response, 'name="body"')  # Verifica que haya un campo para el mensaje
