from django.test import SimpleTestCase
from django.urls import reverse, resolve
from apps.dashboard.views import *

class TestUrls(SimpleTestCase):

    def testUrlDashboardFreelancer(self):
        url = reverse('dashboardFreelancer')
        self.assertEqual(resolve(url).func, dashboardFreelancer)

    def testUrlDashboardClient(self):
        url = reverse('dashboardClient')
        self.assertEqual(resolve(url).func, dashboardClient)

    def testUrlClientAnalysis(self):
        url = reverse('clientAnalysis')
        self.assertEqual(resolve(url).func, clientAnalysis)

    def testUrlFreelancerAnalysis(self):
        url = reverse('freelancerAnalysis')
        self.assertEqual(resolve(url).func, freelancerAnalysis)