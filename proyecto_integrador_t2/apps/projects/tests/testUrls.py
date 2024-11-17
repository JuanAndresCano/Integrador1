from django.test import SimpleTestCase
from django.urls import reverse, resolve
from apps.projects import views

class TestUrls(SimpleTestCase):
    
    def test_create_project_url(self):
        url = reverse('createProject')
        self.assertEqual(resolve(url).func, views.createProject)

    def test_update_project_url(self):
        url = reverse('updateProject', args=['test_pk'])
        self.assertEqual(resolve(url).func, views.updateProject)

    def test_client_project_url(self):
        url = reverse('clientProject')
        self.assertEqual(resolve(url).func, views.clientProject)

    def test_client_deliverable_url(self):
        url = reverse('clientDeliverable', args=['test_pk'])
        self.assertEqual(resolve(url).func, views.clientDeliverable)

    def test_list_freelancer_url(self):
        url = reverse('listFreelancer', args=['test_pk'])
        self.assertEqual(resolve(url).func, views.listFreelancer)

    def test_list_of_freelancers_project_client_url(self):
        url = reverse('listOfFreelancersProjectClient')
        self.assertEqual(resolve(url).func, views.listOfFreelancersProjectClient)

    def test_client_financial_control_url(self):
        url = reverse('clientFinancialControl')
        self.assertEqual(resolve(url).func, views.financial_control)

    def test_gateway_url(self):
        url = reverse('gateWay', args=[1])
        self.assertEqual(resolve(url).func, views.gateWay)

    def test_confirmed_payment_url(self):
        url = reverse('confirmedPayment', args=[1])
        self.assertEqual(resolve(url).func, views.confirmedPayment)

    def test_apply_project_freelancer_url(self):
        url = reverse('applyProjectFreelancer', args=['test_pk'])
        self.assertEqual(resolve(url).func, views.applyProjectFreelancer)

    def test_approve_freelancer_url(self):
        url = reverse('approveFreelancer', args=['test_pk'])
        self.assertEqual(resolve(url).func, views.approveFreelancer)

    def test_reject_freelancer_url(self):
        url = reverse('rejectFreelancer', args=['test_pk'])
        self.assertEqual(resolve(url).func, views.rejectFreelancer)

    def test_approve_profile_freelancer_url(self):
        url = reverse('approveProfileFreelancer', args=['test_pk'])
        self.assertEqual(resolve(url).func, views.approveProfileFreelancer)

    def test_reject_profile_freelancer_url(self):
        url = reverse('rejectProfileFreelancer', args=['test_pk'])
        self.assertEqual(resolve(url).func, views.rejectProfileFreelancer)

    def test_browse_project_url(self):
        url = reverse('browseProject')
        self.assertEqual(resolve(url).func, views.browseProjects)

    def test_browse_own_projects_url(self):
        url = reverse('browseOwnProjects')
        self.assertEqual(resolve(url).func, views.browseOwnProjects)

    def test_information_project_url(self):
        url = reverse('informationProject', args=['test_pk'])
        self.assertEqual(resolve(url).func, views.informationProject)

    def test_add_deliverables_project_url(self):
        url = reverse('addDeliverablesProject', args=['test_pk'])
        self.assertEqual(resolve(url).func, views.addDeliverablesProject)

    def test_add_milestone_deliverable_url(self):
        url = reverse('addMilestoneDeliverable', args=['test_pk'])
        self.assertEqual(resolve(url).func, views.addMilestoneDeliverable)

    def test_delete_milestone_url(self):
        url = reverse('deleteMilestone', args=['test_pk'])
        self.assertEqual(resolve(url).func, views.deleteMilestone)

    def test_delete_deliverable_url(self):
        url = reverse('deleteDeliverable', args=['test_pk'])
        self.assertEqual(resolve(url).func, views.deleteDeliverable)

    def test_send_request_url(self):
        url = reverse('sendRequest', args=['test_pk'])
        self.assertEqual(resolve(url).func, views.sendRequest)

    def test_freelancer_project_url(self):
        url = reverse('freelancerProject')
        self.assertEqual(resolve(url).func, views.freelancerProject)

    def test_deliverables_project_url(self):
        url = reverse('deliverablesProject', args=['test_pk'])
        self.assertEqual(resolve(url).func, views.deliverablesProject)

    def test_freelancer_financial_control_url(self):
        url = reverse('FreelancerFinancialControl')
        self.assertEqual(resolve(url).func, views.freelancerfinancialcontrol)

    def test_apply_project_url(self):
        url = reverse('ApplyProject', args=['test_pk'])
        self.assertEqual(resolve(url).func, views.deliverablesProject)

    def test_add_deliverable_url(self):
        url = reverse('add_deliverable', args=[1])
        self.assertEqual(resolve(url).func, views.add_deliverable)

    def test_apply_for_job_url(self):
        url = reverse('apply_for_job', args=[1])
        self.assertEqual(resolve(url).func, views.apply_for_job)

    def test_client_deliverable_int_pk_url(self):
        url = reverse('clientDeliverable', args=[1])
        self.assertEqual(resolve(url).func, views.clientDeliverable)
