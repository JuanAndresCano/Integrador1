from django.test import TestCase, Client as TestClient  # Importa TestClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from apps.dashboard.views import *
from apps.dashboard.models import *
from apps.accounts.models import *


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

   

    def testFreelancerAccessToDashboardFreelancer(self):
        self.testClient.login(username='freelancerUser', password='testpassword')
        response = self.testClient.get(reverse('dashboardFreelancer'))
        self.assertEqual(response.status_code, 200)

    def testClientAccessToDashboardFreelancer(self):
        self.testClient.login(username='clientUser', password='testpassword')
        response = self.testClient.get(reverse('dashboardFreelancer'))
        self.assertContains(response, 'You are not God to view this page bro')
        self.assertEqual(response.status_code, 200)

    def testUnauthenticatedUserAccessToDashboardFreelancer(self):
        response = self.testClient.get(reverse('dashboardFreelancer'))
        self.assertRedirects(response, '/login/?next=/dashboardFreelancer/')
        self.assertEqual(response.status_code, 302)

    #-------------------------------------------------------------------------------

    def testFreelancerAccessToDashboardClient(self):
        self.testClient.login(username='freelancerUser', password='testpassword')
        response = self.testClient.get(reverse('dashboardClient'))
        self.assertContains(response, 'You are not God to view this page bro')
        self.assertEqual(response.status_code, 200)

    def testClientAccessToDashboardClient(self):
        self.testClient.login(username='clientUser', password='testpassword')
        response = self.testClient.get(reverse('dashboardClient'))
        self.assertEqual(response.status_code, 200)

    def testUnauthenticatedUserAccessToDashboardClient(self):
        response = self.testClient.get(reverse('dashboardClient'))
        self.assertRedirects(response, '/login/?next=/dashboardClient/')
        self.assertEqual(response.status_code, 302)
    
    #-------------------------------------------------------------------------------

    def testFreelancerAccessToClientAnalysis(self):
        self.testClient.login(username='freelancerUser', password='testpassword')
        response = self.testClient.get(reverse('clientAnalysis'))
        self.assertContains(response, 'You are not God to view this page bro')
        self.assertEqual(response.status_code, 200)

    def testClientAccessToClientAnalysis(self):
        self.testClient.login(username='clientUser', password='testpassword')
        response = self.testClient.get(reverse('clientAnalysis'))
        self.assertEqual(response.status_code, 200)

    def testUnauthenticatedUserAccessToClientAnalysis(self):
        response = self.testClient.get(reverse('clientAnalysis'))
        self.assertRedirects(response, '/login/?next=/clientAnalysis/')
        self.assertEqual(response.status_code, 302)

    #-------------------------------------------------------------------------------

    def testFreelancerAccessToFreelancerAnalysis(self):
        self.testClient.login(username='freelancerUser', password='testpassword')
        response = self.testClient.get(reverse('freelancerAnalysis'))
        self.assertEqual(response.status_code, 200)

    def testClientAccessToFreelancerAnalysis(self):
        self.testClient.login(username='clientUser', password='testpassword')
        response = self.testClient.get(reverse('freelancerAnalysis'))
        self.assertContains(response, 'You are not God to view this page bro')
        self.assertEqual(response.status_code, 200)

    def testUnauthenticatedUserAccessToFreelancerAnalysis(self):
        response = self.testClient.get(reverse('freelancerAnalysis'))
        self.assertRedirects(response, '/login/?next=/freelancerAnalysis/')
        self.assertEqual(response.status_code, 302)