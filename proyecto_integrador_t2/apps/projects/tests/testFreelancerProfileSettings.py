from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from datetime import date
from ..models import Freelancer, Portfolio, Experience, FreelancerSkillExpertise, Userk
from django.http import HttpResponse
from ..forms import FreelancerForm, PortfolioForm, ExperienceForm

class FreelancerProfileSettingsTests(TestCase):
    def setUp(self):
        # Crear grupo de freelancer
        self.freelancer_group = Group.objects.create(name='freelancer')
        self.client_group = Group.objects.create(name='client')
        
        # Crear usuario freelancer
        self.freelancer_user = Userk.objects.create_user(
            username='testfreelancer',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        
        # Añadir usuario al grupo freelancer
        self.freelancer_user.groups.add(self.freelancer_group)
        
        # Crear perfil de freelancer
        self.freelancer = Freelancer.objects.create(
            user=self.freelancer_user,
            phoneNumber='1234567890',
            identification='ID123',
            email='test@example.com',
            experience_level='Junior'
        )
        
        # Crear usuario cliente (no freelancer)
        self.client_user = Userk.objects.create_user(
            username='testclient',
            password='testpass123',
            email='client@example.com',
            first_name='Test',
            last_name='Client'
        )
        
        # Añadir usuario al grupo client
        self.client_user.groups.add(self.client_group)
        
        # Crear algunas habilidades
        self.skill1 = FreelancerSkillExpertise.objects.create(name='Python')
        self.skill2 = FreelancerSkillExpertise.objects.create(name='Django')
        self.freelancer.skillExpertises.add(self.skill1, self.skill2)
        
        # Configurar cliente
        self.client = Client()
        
        # URL de la vista
        self.url = reverse('freelancerProfileSettings')
        
        # Crear archivo de prueba para imágenes
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )

    def test_get_profile_settings(self):
        """Prueba la carga inicial de la página de configuración"""
        # Login como freelancer
        self.client.login(username='testfreelancer', password='testpass123')
        
        # Hacer la petición GET
        response = self.client.get(self.url)
        
        # Verificar código de respuesta
        self.assertEqual(response.status_code, 200)
        
        # Verificar que la respuesta contiene los formularios necesarios
        self.assertIsInstance(response.context['form'], FreelancerForm)
        self.assertIsInstance(response.context['portfolio_form'], PortfolioForm)
        self.assertIsInstance(response.context['experience_form'], ExperienceForm)
        
        # Verificar que el freelancer es correcto en el contexto
        self.assertEqual(response.context['freelancer'], self.freelancer)
        
        # Verificar que se usa el template correcto
        self.assertTemplateUsed(response, 'freelancerProfileSettings.html')

    def test_update_profile(self):
        """Prueba la actualización del perfil del freelancer"""
        self.client.login(username='testfreelancer', password='testpass123')
        
        # Preparar los datos del formulario
        form_data = {
            'phoneNumber': '9876543210',
            'identification': '132112312',
            'email': 'new@example.com',
            'experience_level': 'Senior',
            'description': 'Nueva descripción',
            'linkedin_url': 'https://linkedin.com/in/test',
            'new_skills': 'React,Node.js',
            'github_url': 'https://github.com/test',
            'instagram_url': 'https://instagram.com/test'
        }
        
        # Realizar la petición POST
        response = self.client.post(self.url, form_data)
        
        # Verificar redirección
        self.assertRedirects(response, self.url)
        
        # Recargar el freelancer desde la base de datos
        updated_freelancer = Freelancer.objects.get(id=self.freelancer.id)
        
        # Verificar que los campos se actualizaron correctamente
        self.assertEqual(updated_freelancer.phoneNumber, '9876543210')
        self.assertEqual(updated_freelancer.email, 'new@example.com')
        self.assertEqual(updated_freelancer.experience_level, 'Senior')
        self.assertEqual(updated_freelancer.description, 'Nueva descripción')
        self.assertEqual(updated_freelancer.linkedin_url, 'https://linkedin.com/in/test')
        self.assertEqual(updated_freelancer.github_url, 'https://github.com/test')
        self.assertEqual(updated_freelancer.instagram_url, 'https://instagram.com/test')
        
        # Verificar que las nuevas habilidades se agregaron
        self.assertTrue(updated_freelancer.skillExpertises.filter(name__in=['React', 'Node.js']).exists())

    def test_add_portfolio(self):
        """Prueba la adición de un proyecto al portafolio"""
        self.client.login(username='testfreelancer', password='testpass123')
        
        # Preparar datos del portafolio
        portfolio_data = {
            'project_name': 'Test Project',
            'project_description': 'Test Description',
            'project_duration_months': 6,
            'project_link': 'https://example.com/project'
        }
        
        if self.test_image:
            portfolio_data['project_image'] = self.test_image
        
        # Realizar la petición POST
        response = self.client.post(self.url, portfolio_data)
        
        # Verificar la redirección
        self.assertRedirects(response, self.url)
        
        # Verificar que el portafolio fue creado
        portfolio = Portfolio.objects.filter(
            freelancer=self.freelancer,
            project_name='Test Project'
        ).first()
        
        self.assertIsNotNone(portfolio)
        self.assertEqual(portfolio.project_description, 'Test Description')
        self.assertEqual(portfolio.project_duration_months, 6)
        self.assertEqual(portfolio.project_link, 'https://example.com/project')