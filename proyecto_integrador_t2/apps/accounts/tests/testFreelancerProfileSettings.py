from django.test import TestCase
from django.urls import reverse
from datetime import date
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from django.contrib.auth import get_user_model
from apps.accounts.models import Freelancer, Portfolio, Experience, FreelancerSkillExpertise, Client, Rating

User = get_user_model()

class FreelancerProfileSettingsTest(TestCase):
    def setUp(self):
        """
        Configura los datos iniciales para las pruebas.
        Crea un usuario freelancer y un cliente para las pruebas de perfil.
        """
        self.freelancer_user = User.objects.create_user(username='freelanceruser', password='testpass', is_freelancer=True)
        self.freelancer_profile = Freelancer.objects.create(user=self.freelancer_user, phoneNumber="987654321")

        self.client_user = User.objects.create_user(username='clientuser', password='testpass', is_client=True)
        self.client_profile = Client.objects.create(user=self.client_user, phoneNumber="123456789")

        self.freelancer_url = reverse('freelancerProfileSettings')

        self.client.login(username='freelanceruser', password='testpass')

        # Definir un archivo de prueba para el campo 'resume'
        self.resume_file = SimpleUploadedFile("resume.pdf", b"PDF content", content_type="application/pdf")

    def testGetFreelancerProfile(self):
        """
        Verifica que la página de configuración del perfil de freelancer se carga correctamente.
        """
        response = self.client.get(self.freelancer_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/freelancerProfileSettings.html')

    def testUpdateFreelancerProfile(self):
        """
        Verifica que se puede actualizar el perfil de freelancer correctamente.
        """
        # Añadir nuevas habilidades para mostrar en el perfil
        self.expertise_1 = FreelancerSkillExpertise.objects.create(name="Javascript")
        self.expertise_2 = FreelancerSkillExpertise.objects.create(name="SQL")
        self.expertise_3 = FreelancerSkillExpertise.objects.create(name="NodeJs")
        self.expertise_4 = FreelancerSkillExpertise.objects.create(name="Cassandra")
        
        # Preparar los datos del formulario para actualizar el perfil
        form_data = {
            "description": "Experienced SQL and noSQL developer",
            "experience_level": "Senior",
            "linkedin_url": "https://linkedin.com/in/freelancer_test",
            "github_url": "https://github.com/freelancer_test",
            "instagram_url": "",  # Campo opcional
            "resume": self.resume_file,
            "skillExpertises": [self.expertise_1.id, self.expertise_2.id, self.expertise_3.id, self.expertise_4.id]
        }

        # Enviar la solicitud POST para actualizar el perfil
        response = self.client.post(self.freelancer_url, form_data)
        
        # Verificar redirección después de la actualización exitosa
        self.assertEqual(response.status_code, 302)

        self.freelancer_profile.refresh_from_db()

        # Verificar que los datos fueron actualizados correctamente
        self.assertEqual(self.freelancer_profile.description, "Experienced SQL and noSQL developer")
        self.assertEqual(self.freelancer_profile.experience_level, "Senior")
        self.assertEqual(self.freelancer_profile.linkedin_url, "https://linkedin.com/in/freelancer_test")
        self.assertEqual(self.freelancer_profile.github_url, "https://github.com/freelancer_test")
        self.assertTrue(self.freelancer_profile.resume.name.startswith('resumes/resume'))

        # Verificar que todas las habilidades añadidas están en el perfil del freelancer
        self.assertIn(self.expertise_1, self.freelancer_profile.skillExpertises.all())
        self.assertIn(self.expertise_2, self.freelancer_profile.skillExpertises.all())
        self.assertIn(self.expertise_3, self.freelancer_profile.skillExpertises.all())
        self.assertIn(self.expertise_4, self.freelancer_profile.skillExpertises.all())


    def testUpdateFreelancerProfileWithSpecialCharacters(self):
        """
        Verifica que la descripción del perfil pueda contener caracteres especiales.
        """

        self.expertise_1 = FreelancerSkillExpertise.objects.create(name="Javascript")

        special_description = "Developer & Engineer at XYZ, specializing in Python, C++, and SQL."

        form_data = {
            "description": special_description,
            "experience_level": "Senior",
            "linkedin_url": "https://linkedin.com/in/freelancer_test",
            "github_url": "https://github.com/freelancer_test",
            "resume": self.resume_file,
            "skillExpertises": [self.expertise_1.id]
        }

        response = self.client.post(self.freelancer_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.freelancer_profile.refresh_from_db()
        self.assertEqual(self.freelancer_profile.description, special_description)

    def testAddExperienceFreelancerProfile(self):
        """
        Verifica que se puede añadir experiencia al perfil de freelancer.
        """
        self.experience1 = Experience.objects.create(
            freelancer=self.freelancer_profile,
            job="Tester",
            company="Amazonas",
            start_date=date(2020, 5, 1),
            end_date=date(2023, 5, 1),
            job_description="Unitary and Automatic testing for Amazonas company"
        )

    def testUpdateExperience(self):
        """
        Verifica que se pueden actualizar los datos de experiencia en el perfil de freelancer.
        """
        experience = Experience.objects.create(
            freelancer=self.freelancer_profile,
            job="Developer",
            company="Company A",
            start_date=date(2020, 1, 1),
            end_date=date(2022, 1, 1),
            job_description="Development work"
        )

    def testRemoveExperienceFreelancerProfile(self):
        """
        Verifica que un freelancer pueda eliminar una experiencia laboral de su perfil.
        """
        # Crear una experiencia
        experience = Experience.objects.create(
            freelancer=self.freelancer_profile,
            job="Tester",
            company="Amazonas",
            start_date=date(2020, 5, 1),
            end_date=date(2023, 5, 1),
            job_description="Unitary testing for Amazonas"
        )

        # Eliminar la experiencia
        experience.delete()

        # Verificar que la experiencia fue eliminada
        self.assertFalse(Experience.objects.filter(id=experience.id).exists())

        # Actualizar algunos datos de la experiencia
        experience.job = "Senior Developer"
        experience.job_description = "Lead development projects"
        experience.save()

        # Refrescar y verificar cambios
        experience.refresh_from_db()
        self.assertEqual(experience.job, "Senior Developer")
        self.assertEqual(experience.job_description, "Lead development projects")

        # Verificar que la experiencia ha sido vinculada al freelancer
        self.assertEqual(experience.freelancer, self.freelancer_profile)

    def testAddPortfolioFreelancerProfile(self):
        """
        Verifica que se puede añadir un proyecto al portafolio del freelancer.
        """
        self.portfolio1 = Portfolio.objects.create(
            freelancer=self.freelancer_profile,
            project_name="Testing",
            project_description="This project is a test",
            project_duration_months="50",
            project_link="https://github.com/freelancer_test"
        )

        # Verificar que el portafolio ha sido vinculado al freelancer
        self.assertEqual(self.portfolio1.freelancer, self.freelancer_profile)

    def testEditPortfolioProject(self):
        """
        Verifica que se pueda editar un proyecto existente en el portafolio del freelancer.
        """
        # Crear un proyecto de portafolio
        portfolio = Portfolio.objects.create(
            freelancer=self.freelancer_profile,
            project_name="Old Project",
            project_description="This is an old project",
            project_duration_months="12",
            project_link="https://github.com/old_project"
        )

        # Editar el proyecto
        portfolio.project_name = "Updated Project"
        portfolio.project_description = "This is an updated project"
        portfolio.save()

        # Verificar los cambios
        portfolio.refresh_from_db()
        self.assertEqual(portfolio.project_name, "Updated Project")
        self.assertEqual(portfolio.project_description, "This is an updated project")

    def testRemovePortfolioProject(self):
        """
        Verifica que se puede eliminar un proyecto del portafolio de un freelancer.
        """
        # Crear un proyecto en el portafolio
        portfolio = Portfolio.objects.create(
            freelancer=self.freelancer_profile,
            project_name="Old Project",
            project_description="This is an old project",
            project_duration_months="12",
            project_link="https://github.com/old_project"
        )

        portfolio.delete()
        self.assertFalse(Portfolio.objects.filter(id=portfolio.id).exists())

    def testAddRatingFreelancerProfile(self):
        """
        Verifica que se puede añadir una calificación al perfil del freelancer.
        """
        # Crear y asignar un rating al freelancer por parte del cliente
        self.rating = Rating.objects.create(
            freelancer=self.freelancer_profile,
            client=self.client_profile,
            rating=5,  # Calificación entre 1 y 5
            comment='Excelente trabajo realizado por el freelancer.',
            date_posted=timezone.now()
        )

        # Verificar que el rating se creó correctamente y está vinculado al freelancer y al cliente
        self.assertEqual(self.rating.freelancer, self.freelancer_profile)
        self.assertEqual(self.rating.client, self.client_profile)
        self.assertEqual(self.rating.rating, 5)
        self.assertEqual(self.rating.comment, 'Excelente trabajo realizado por el freelancer.')
        self.assertIsNotNone(self.rating.date_posted)

    def testUpdateRatingWithFreelancerResponse(self):
        """
        Verifica que se puede actualizar un rating con una respuesta del freelancer.
        """
        # Crear un rating inicial sin respuesta del freelancer
        self.rating = Rating.objects.create(
            freelancer=self.freelancer_profile,
            client=self.client_profile,
            rating=4,
            comment='Buen trabajo en general, pero hay áreas de mejora.',
            date_posted=timezone.now()
        )

        # Actualizar el rating para añadir una respuesta del freelancer
        freelancer_response = '¡Gracias por tu feedback! Trabajaré en mejorar esos puntos.'
        self.rating.response = freelancer_response
        self.rating.save()

        # Refrescar el objeto desde la base de datos para asegurarnos de que el cambio fue guardado
        self.rating.refresh_from_db()

        # Verificar que la respuesta del freelancer se guardó correctamente
        self.assertEqual(self.rating.response, freelancer_response)

        # Confirmar que el resto de los datos no se han modificado
        self.assertEqual(self.rating.freelancer, self.freelancer_profile)
        self.assertEqual(self.rating.client, self.client_profile)
        self.assertEqual(self.rating.rating, 4)
        self.assertEqual(self.rating.comment, 'Buen trabajo en general, pero hay áreas de mejora.')
        self.assertEqual(self.rating.response, '¡Gracias por tu feedback! Trabajaré en mejorar esos puntos.')

    def testDeleteRating(self):
        """
        Verifica que se puede eliminar un rating del perfil del freelancer.
        """
        rating = Rating.objects.create(
            freelancer=self.freelancer_profile,
            client=self.client_profile,
            rating=4,
            comment='Great work!',
            date_posted=timezone.now()
        )

        # Eliminar el rating
        rating.delete()

        # Verificar que el rating ha sido eliminado
        self.assertFalse(Rating.objects.filter(id=rating.id).exists())