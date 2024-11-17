from django.test import TestCase, Client as TestClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.accounts.models import *
from django.contrib.auth import authenticate
from apps.projects.models import *

class TestAuthentication(TestCase):

    def setUp(self):
        # Crear los usuarios para las pruebas
        self.clientUser = Userk.objects.create_user(username='clientUser', password='testpassword', is_client=True)
        self.freelancerUser = Userk.objects.create_user(username='freelancerUser', password='testpassword', is_freelancer=True)

        # Crear instancias de Client y Freelancer asociadas a los usuarios
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

        # Crear un skill expertise y una complejidad para el proyecto
        skill_expertise = ProjectSkillExpertise.objects.create(name='Python Developer')
        complexity = ProjectComplexity.objects.create(levelName='Intermediate', description='Intermediate level required')

        # Crear un proyecto
        self.project = Project.objects.create(
            title='Test Project',
            description='A description of the test project',
            client=self.testClientInstance,
            requiredPosition='Developer',
            daysDuration=30,
            budget=1000.00,
            complexity=complexity,
        )
        
        self.project.skillExpertises.add(skill_expertise)

        # Crear un ProjectContributor
        self.projectContributor = ProjectContributor.objects.create(
            project=self.project,
            freelancer=self.freelancer,
            title='Contributor',
            requiredPosition='Developer',
            budget=500.00,
            daysDuration=15,
            complexity=complexity,
            version=1,
            project_status='PENDING',
            approval_status='pending',
            rejectionReason='pending',
        )

        # URLs para las pruebas
        self.client_register_url = reverse('clientRegister')
        self.freelancer_register_url = reverse('freelancerRegister')
        self.landpage_url = reverse('landpage')
        self.login_url = reverse('login')
        self.client_profile_url = reverse('clientProfile')
        self.freelancer_profile_url = reverse('freelancerProfile', args=[self.freelancerUser.id])
        self.fprofile_request_url = reverse('fprofileRequest', args=[self.freelancerUser.id, '123'])
        self.freelancer_profile_settings_url = reverse('freelancerProfileSettings')
    

    def testClientAccessToLogIn(self):
        self.client.login(username='clientUser', password='testpassword')  # Usando self.testClient
        response = self.client.get(self.login_url)
        self.assertRedirects(response, '/clientProject/')
        self.assertEqual(response.status_code, 302)

    def testFreelancerAccessToLogIn(self):
        self.client.login(username='freelancerUser', password='testpassword')  # Usando self.testClient
        response = self.client.get(self.login_url)
        self.assertRedirects(response, '/browseProject/')
        self.assertEqual(response.status_code, 302)

    def testUnauthenticatedUserAccessToLogIn(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    # Tests para el registro de cliente
    def testClientAccessToClientRegister(self):
        """Verifica que un cliente logueado es redirigido a clientProject"""
        self.client.login(username='clientUser', password='testpassword')
        response = self.client.get(self.client_register_url)
        self.assertRedirects(response, '/clientProject/')
        self.assertEqual(response.status_code, 302)

    def testFreelancerAccessToClientRegister(self):
        """Verifica que un freelancer logueado es redirigido a browseProject"""
        self.client.login(username='freelancerUser', password='testpassword')
        response = self.client.get(self.client_register_url)
        self.assertRedirects(response, '/browseProject/')
        self.assertEqual(response.status_code, 302)

    def testUnauthenticatedUserAccessToClientRegister(self):
        """Verifica que un usuario no logueado puede acceder a clientRegister"""
        response = self.client.get(self.client_register_url)
        self.assertEqual(response.status_code, 200)

    # Tests para el registro de freelancer
    def testClientAccessToFreelancerRegister(self):
        """Verifica que un cliente logueado es redirigido a clientProject"""
        self.client.login(username='clientUser', password='testpassword')
        response = self.client.get(self.freelancer_register_url)
        self.assertRedirects(response, '/clientProject/')
        self.assertEqual(response.status_code, 302)

    def testFreelancerAccessToFreelancerRegister(self):
        """Verifica que un freelancer logueado no se redirige, debe ver la página"""
        self.client.login(username='freelancerUser', password='testpassword')
        response = self.client.get(self.freelancer_register_url)
        self.assertEqual(response.status_code, 302)

    def testUnauthenticatedUserAccessToFreelancerRegister(self):
        """Verifica que un usuario no logueado puede acceder a freelancerRegister"""
        response = self.client.get(self.freelancer_register_url)
        self.assertEqual(response.status_code, 200)

    # Tests para la página de inicio (landpage)
    def testClientAccessToLandpage(self):
        """Verifica que un cliente logueado es redirigido a clientProject"""
        self.client.login(username='clientUser', password='testpassword')
        response = self.client.get(self.landpage_url)
        self.assertRedirects(response, '/clientProject/')
        self.assertEqual(response.status_code, 302)

    def testFreelancerAccessToLandpage(self):
        """Verifica que un freelancer logueado es redirigido a browseProject"""
        self.client.login(username='freelancerUser', password='testpassword')
        response = self.client.get(self.landpage_url)
        self.assertRedirects(response, '/browseProject/')
        self.assertEqual(response.status_code, 302)

    def testUnauthenticatedUserAccessToLandpage(self):
        """Verifica que un usuario no logueado puede acceder a landpage"""
        response = self.client.get(self.landpage_url)
        self.assertEqual(response.status_code, 200)

#-------------------------------------------------------------------------------------

    # Tests para clientProfile
    def testClientAccessToClientProfile(self):
        """Verifica que un cliente logueado puede acceder a su perfil"""
        self.client.login(username='clientUser', password='testpassword')
        response = self.client.get(self.client_profile_url)
        self.assertEqual(response.status_code, 200)

    def testFreelancerAccessToClientProfile(self):
        """Verifica que un freelancer logueado es redirigido a clientProject"""
        self.client.login(username='freelancerUser', password='testpassword')
        response = self.client.get(self.client_profile_url)
        self.assertContains(response, 'You are not God to view this page bro')
        self.assertEqual(response.status_code, 200)

    def testUnauthenticatedUserAccessToClientProfile(self):
        """Verifica que un usuario no autenticado es redirigido a login"""
        response = self.client.get(self.client_profile_url)
        self.assertRedirects(response, '/login/?next=/profile/')
        self.assertEqual(response.status_code, 302)

    # Tests para freelancerProfile
    def testClientAccessToFreelancerProfile(self):
        """Verifica que un cliente logueado puede acceder al perfil de un freelancer"""
        self.client.login(username='clientUser', password='testpassword')
        response = self.client.get(self.freelancer_profile_url)
        self.assertEqual(response.status_code, 200)

    def testFreelancerAccessToFreelancerProfile(self):
        """Verifica que un freelancer logueado puede acceder a su propio perfil"""
        self.client.login(username='freelancerUser', password='testpassword')
        response = self.client.get(self.freelancer_profile_url)
        self.assertEqual(response.status_code, 200)
    
    def testUnauthenticatedUserAccessToFreelancerProfile(self):
        """Verifica que un usuario no autenticado es redirigido a login"""
        response = self.client.get(self.freelancer_profile_url)
        self.assertRedirects(response, '/login/?next=/fprofile/{}/'.format(self.freelancerUser.id))
        self.assertEqual(response.status_code, 302)
    
    # Tests para fprofileRequest
    def testClientAccessToFprofileRequest(self):
        """Verifica que un cliente logueado puede hacer una solicitud de perfil"""
        self.client.login(username='clientUser', password='testpassword')

        # Obtener el ID del projectContributor para incluirlo en la URL
        project_contributor_id = self.projectContributor.id
        # Usar el pk del freelancer desde la instancia del modelo
        freelancer_pk = self.freelancer.user.id

        # Pasar pk y contributorId en la URL
        response = self.client.get(reverse('fprofileRequest', args=[freelancer_pk, project_contributor_id]))
        self.assertEqual(response.status_code, 200)

    def testFreelancerAccessToFprofileRequest(self):
        """Verifica que un freelancer logueado no puede acceder a la página"""
        self.client.login(username='freelancerUser', password='testpassword')

        # Obtener el ID del projectContributor para incluirlo en la URL
        project_contributor_id = self.projectContributor.id
        # Usar el pk del freelancer desde la instancia del modelo
        freelancer_pk = self.freelancer.user.id

        # Pasar pk y contributorId en la URL
        response = self.client.get(reverse('fprofileRequest', args=[freelancer_pk, project_contributor_id]))
        
        # Comprobar el mensaje de error adecuado
        self.assertContains(response, 'You are not God to view this page bro')
        self.assertEqual(response.status_code, 200)

    def testUnauthenticatedUserAccessToFprofileRequest(self):
        """Verifica que un usuario no autenticado es redirigido a login"""
        # Obtener el ID del projectContributor para incluirlo en la URL
        project_contributor_id = self.projectContributor.id
        # Usar el pk del freelancer desde la instancia del modelo
        freelancer_pk = self.freelancer.user.id

        # Pasar pk y contributorId en la URL
        response = self.client.get(reverse('fprofileRequest', args=[freelancer_pk, project_contributor_id]))
        
        # Verificar la redirección
        self.assertRedirects(response, f'/login/?next=/fprofileRequest/{freelancer_pk}/{project_contributor_id}/')
        self.assertEqual(response.status_code, 302)


    # Tests para freelancerProfileSettings
    def testFreelancerAccessToFreelancerProfileSettings(self):
        """Verifica que un freelancer logueado puede acceder a la configuración de su perfil"""
        self.client.login(username='freelancerUser', password='testpassword')
        response = self.client.get(self.freelancer_profile_settings_url)
        self.assertEqual(response.status_code, 200)

    def testClientAccessToFreelancerProfileSettings(self):
        """Verifica que un cliente logueado es redirigido a clientProject"""
        self.client.login(username='clientUser', password='testpassword')
        response = self.client.get(self.freelancer_profile_settings_url)
        self.assertContains(response, 'You are not God to view this page bro')
        self.assertEqual(response.status_code, 200)

    def testUnauthenticatedUserAccessToFreelancerProfileSettings(self):
        """Verifica que un usuario no autenticado es redirigido a login"""
        response = self.client.get(self.freelancer_profile_settings_url)
        self.assertRedirects(response, '/login/?next=/fprofileSettings/')
        self.assertEqual(response.status_code, 302)

    