from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.projects.models import Project, ProjectComplexity, ProjectSkillExpertise, ProjectContributor
from apps.accounts.models import Freelancer, Client as ClientModel

User = get_user_model()

class TestBrowseProjects(TestCase):
    def setUp(self):
        # Create a freelancer user and a client user
        self.freelancer_user = User.objects.create_user(username="freelancer1", password="testpassword", is_freelancer=True)
        self.client_user = User.objects.create_user(username="client1", password="clientpassword", is_client=True)
        
        # Create Freelancer and Client objects
        self.freelancer = Freelancer.objects.create(user=self.freelancer_user, phoneNumber="123456789", identification="1234")
        self.client = ClientModel.objects.create(user=self.client_user, phoneNumber="987654321", taxId="5678", companyName="Test Client Co")

        # Create instances of ProjectComplexity and ProjectSkillExpertise
        self.complexity = ProjectComplexity.objects.create(levelName="Intermediate", description="Medium complexity")
        self.skill_expertise = ProjectSkillExpertise.objects.create(name="Python")

        # Create test projects
        self.project1 = Project.objects.create(
            title="Project A",
            description="Description for project A",
            requiredPosition="Developer",
            daysDuration=30,
            budget="1500.00",
            complexity=self.complexity,
            client=self.client,
        )
        self.project1.skillExpertises.add(self.skill_expertise)

        self.project2 = Project.objects.create(
            title="Project B",
            description="Description for project B",
            requiredPosition="Designer",
            daysDuration=60,
            budget="2500.00",
            complexity=self.complexity,
            client=self.client,
        )
        self.project2.skillExpertises.add(self.skill_expertise)

        # Authenticate the freelancer in the test client
        self.client = Client()
        self.client.login(username="freelancer1", password="testpassword")

    def test_browse_projects(self):
        """
        Test that the `browseProjects` view correctly lists projects.
        """
        url = reverse("browseProject")
        response = self.client.get(url)

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that both projects are in the context
        self.assertIn(self.project1, response.context["projects"])
        self.assertIn(self.project2, response.context["projects"])

    def test_browse_projects_with_filtering(self):
        """
        Test that filters applied to the `browseProjects` view work.
        """
        url = reverse("browseProject")
        response = self.client.get(url, {"sort_by": "title"})

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Ensure that the first project in the list is ordered by title
        projects = response.context["projects"]
        self.assertEqual(projects[0].title, "Project A")
        self.assertEqual(projects[1].title, "Project B")

    def test_browse_own_projects(self):
        """
        Test that the `browseOwnProjects` view only lists applied and approved projects.
        """
        # Create an approved ProjectContributor associated with `project1`
        ProjectContributor.objects.create(
            title="Contributor for Project A",
            requiredPosition="Developer",
            budget=1200.00,
            complexity=self.complexity,
            project=self.project1,
            freelancer=self.freelancer,
            approval_status="approved",
            version=1
        )

        url = reverse("browseOwnProjects")
        response = self.client.get(url)

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Verify that only the applied and approved project is in the context
        self.assertIn(self.project1, response.context["projects"])
        self.assertNotIn(self.project2, response.context["projects"])

    def test_browse_own_projects_not_approved(self):
        """
        Test that `browseOwnProjects` does not list unapproved projects.
        """
        # Create an unapproved ProjectContributor
        ProjectContributor.objects.create(
            title="Contributor for Project B",
            requiredPosition="Developer",
            budget=1200.00,
            complexity=self.complexity,
            project=self.project2,
            freelancer=self.freelancer,
            approval_status="pending",  # Unapproved project
            version=1
        )

        url = reverse("browseOwnProjects")
        response = self.client.get(url)

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Verify that the unapproved project does not appear
        self.assertNotIn(self.project2, response.context["projects"])

    def test_browse_own_projects_with_sorting(self):
        """
        Test that sorting in `browseOwnProjects` works correctly.
        """
        # Create approved ProjectContributors for both projects
        ProjectContributor.objects.create(
            title="Contributor for Project A",
            requiredPosition="Developer",
            budget=1500.00,
            complexity=self.complexity,
            project=self.project1,
            freelancer=self.freelancer,
            approval_status="approved",
            version=1
        )

        ProjectContributor.objects.create(
            title="Contributor for Project B",
            requiredPosition="Designer",
            budget=2000.00,
            complexity=self.complexity,
            project=self.project2,
            freelancer=self.freelancer,
            approval_status="approved",
            version=1
        )

        url = reverse("browseOwnProjects")
        response = self.client.get(url, {"sort_by": "title"})

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Ensure that the first project in the list is ordered by title
        projects = response.context["projects"]
        self.assertEqual(projects[0].title, "Project A")
        self.assertEqual(projects[1].title, "Project B")

