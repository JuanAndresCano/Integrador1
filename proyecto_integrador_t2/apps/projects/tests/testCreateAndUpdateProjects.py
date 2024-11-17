from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.projects.models import Project, ProjectComplexity, ProjectSkillExpertise
from apps.accounts.models import Client as ClientModel

User = get_user_model()

class testCreateAndUpdateProjects(TestCase):

    def setUp(self):
        # Crear un usuario cliente y un objeto Client
        self.user = User.objects.create_user(username="testclient", password="testpassword", is_client=True)
        self.client_user = ClientModel.objects.create(
            user=self.user,
            phoneNumber="123456789",
            taxId="1234",
            companyName="Test Company",
            typeOfCompany="Software",
            businessVertical="Technology",
            countryOfLocation="USA",
            city="New York",
            address="123 Test St",
            description_company="Test description"
        )

        # Crear instancias de ProjectComplexity y ProjectSkillExpertise
        self.complexity = ProjectComplexity.objects.create(levelName="Intermediate", description="Medium complexity")
        self.skill_expertise = ProjectSkillExpertise.objects.create(name="Python")
        
        # Autenticar al cliente en el cliente de pruebas
        self.client.login(username="testclient", password="testpassword")

    def test_create_project_missing_field(self):
        url = reverse("createProject")
        data = {
            "description": "Project without title",
            "requiredPosition": "Developer",
            "daysDuration": 30,
            "budget": "1500.00",
            "complexity": self.complexity.id,
            "skillExpertises": [self.skill_expertise.id],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # Debe fallar la creación
        #self.assertContains(response, "Este campo es obligatorio")  # Verifica mensaje de error

    def test_update_project_invalid_budget(self):
        project = Project.objects.create(
            title="Project",
            description="Description",
            requiredPosition="Developer",
            daysDuration=30,
            budget="1500.00",
            complexity=self.complexity,
            client=self.client_user,
            version=1
        )
        project.skillExpertises.add(self.skill_expertise)
        url = reverse("updateProject", args=[project.id])
        update_data = {
            "title": "Updated Project",
            "description": "Updated description",
            "requiredPosition": "Senior Developer",
            "daysDuration": 25,
            "budget": "invalid_budget",
            "complexity": self.complexity.id,
            "skillExpertises": [self.skill_expertise.id],
        }
        response = self.client.post(url, update_data)
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, "Introduzca un número válido")

    def test_update_project_skill_expertise(self):
        project = Project.objects.create(
            title="Project",
            description="Description",
            requiredPosition="Designer",
            daysDuration=30,
            budget="1000.00",
            complexity=self.complexity,
            client=self.client_user,
            version=1
        )
        project.skillExpertises.add(self.skill_expertise)
        new_skill = ProjectSkillExpertise.objects.create(name="Django")
        url = reverse("updateProject", args=[project.id])
        update_data = {
            "title": "Updated Project",
            "description": "Updated description",
            "requiredPosition": "Designer",
            "daysDuration": 30,
            "budget": "1000.00",
            "complexity": self.complexity.id,
            "skillExpertises": [new_skill.id],
        }
        response = self.client.post(url, update_data)
        project.refresh_from_db()
        self.assertIn(new_skill, project.skillExpertises.all())
        self.assertNotIn(self.skill_expertise, project.skillExpertises.all())

    def test_create_project_redirect_authenticated_user(self):
        url = reverse("createProject")
        data = {
            "title": "New Authenticated Project",
            "description": "Description",
            "requiredPosition": "Developer",
            "daysDuration": 30,
            "budget": "2000.00",
            "complexity": self.complexity.id,
            "skillExpertises": [self.skill_expertise.id],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("clientProject"))

    def test_create_project_unauthenticated_user(self):
        self.client.logout()  # Salir del cliente autenticado
        url = reverse("createProject")
        response = self.client.get(url)
        self.assertRedirects(response, "/login/?next=/createProject/")

    def test_update_project_unauthorized_user(self):
        project = Project.objects.create(
            title="Unauthorized Update",
            description="Description",
            requiredPosition="Developer",
            daysDuration=10,
            budget="500.00",
            complexity=self.complexity,
            client=self.client_user,
            version=1
        )
        project.skillExpertises.add(self.skill_expertise)
        self.client.logout()
        url = reverse("updateProject", args=[project.id])
        response = self.client.get(url)
        self.assertRedirects(response, f"/login/?next=/updateProject/{project.id}/")

    def test_project_version_increment_on_update(self):
        project = Project.objects.create(
            title="Versioned Project",
            description="Initial description",
            requiredPosition="Project Manager",
            daysDuration=40,
            budget="3000.00",
            complexity=self.complexity,
            client=self.client_user,
            version=1
        )
        project.skillExpertises.add(self.skill_expertise)
        url = reverse("updateProject", args=[project.id])
        update_data = {
            "title": "Updated Versioned Project",
            "description": "Updated description",
            "requiredPosition": "Project Manager",
            "daysDuration": 40,
            "budget": "3000.00",
            "complexity": self.complexity.id,
            "skillExpertises": [self.skill_expertise.id],
        }
        self.client.post(url, update_data)
        project.refresh_from_db()
        self.assertEqual(project.version, 2)

    def test_create_project_with_multiple_skills(self):
        new_skill = ProjectSkillExpertise.objects.create(name="JavaScript")
        url = reverse("createProject")
        data = {
            "title": "Multi-skilled Project",
            "description": "Project with multiple skills",
            "requiredPosition": "Full Stack Developer",
            "daysDuration": 45,
            "budget": "3500.00",
            "complexity": self.complexity.id,
            "skillExpertises": [self.skill_expertise.id, new_skill.id],
        }
        response = self.client.post(url, data)
        project = Project.objects.get(title="Multi-skilled Project")
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.skill_expertise, project.skillExpertises.all())
        self.assertIn(new_skill, project.skillExpertises.all())

