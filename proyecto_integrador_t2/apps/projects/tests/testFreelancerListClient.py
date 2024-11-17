from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.projects.models import Project, ProjectComplexity, ProjectSkillExpertise, ProjectContributor
from apps.accounts.models import Freelancer, Client as ClientModel

User = get_user_model()

class TestListFreelancer(TestCase):
    def setUp(self):
        # Create a freelancer user and a client user
        self.freelancer_user = User.objects.create_user(username="freelancer1", password="testpassword", is_freelancer=True)
        self.freelancer = Freelancer.objects.create(user=self.freelancer_user, phoneNumber="123456789", identification="1234")

        self.client_user = User.objects.create_user(username="testclient", password="testpassword", is_client=True)
        self.client = ClientModel.objects.create(
            user=self.client_user,
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

        # Create instances of ProjectComplexity and ProjectSkillExpertise
        self.complexity = ProjectComplexity.objects.create(levelName="Intermediate", description="Medium complexity")
        self.skill_expertise = ProjectSkillExpertise.objects.create(name="Python")

        # Create test project
        self.project1 = Project.objects.create(
            title="Project A",
            description="Description for project A",
            requiredPosition="Developer",
            daysDuration=30,
            budget="1500.00",
            complexity=self.complexity,
            client=self.client,
            version=1
        )
        self.project1.skillExpertises.add(self.skill_expertise)

        # Create a ProjectContributor to associate the freelancer with the project
        self.project_contributor1 = ProjectContributor.objects.create(
            title="Developer",
            description="Freelancer applying for project A",
            requiredPosition="Developer",
            project=self.project1,
            freelancer=self.freelancer,
            approval_status="approved",
            is_send=True,
            version=1
        )

        self.project_contributor2 = ProjectContributor.objects.create(
            title="Designer",
            description="Freelancer applying for project A",
            requiredPosition="Designer",
            project=self.project1,
            freelancer=self.freelancer,
            approval_status="rejected",
            is_send=False,
            version=1
        )

        # Log in the client user
        self.client = Client()
        self.client.login(username="testclient", password="testpassword")

        # Use the correct URL reversal with pk
        self.freelancer_url = reverse('listFreelancer', kwargs={'pk': self.project1.id})

    def testGetFreelancerList(self):
        """
        Verifica que la página de freelancer list se carga correctamente.
        """
        response = self.client.get(self.freelancer_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/listFreelancer.html')

    def test_client_can_view_approved_freelancers(self):
        # Get the list of freelancers associated with the project using correct reverse URL with pk
        response = self.client.get(reverse("listFreelancer", kwargs={'pk': self.project1.id}))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the approved and sent ProjectContributor is displayed
        self.assertContains(response, self.project_contributor1.title)
        self.assertContains(response, self.freelancer.user.username)
        self.assertContains(response, str(self.project_contributor1.progress) + "%")

        # Check that the rejected or unsent ProjectContributor is not displayed
        self.assertNotContains(response, self.project_contributor2.title)