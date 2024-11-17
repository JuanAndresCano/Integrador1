from django.test import SimpleTestCase
from django.urls import reverse, resolve
from apps.communications.views import *

class TestUrls(SimpleTestCase):

    def testUrlFreelancerMessageHome(self):
        url = reverse('freelancerMessageHome')
        self.assertEqual(resolve(url).func, freelancerMessageHome)

    def testUrlClientMessageHome(self):
        url = reverse('clientMessageHome')
        self.assertEqual(resolve(url).func, clientMessageHome)

    def testUrlFreelancerMessage(self):
        url = reverse('freelancerMessage', args=['testChatName'])
        self.assertEqual(resolve(url).func, freelancerMessage)

    def testUrlClientMessage(self):
        url = reverse('clientMessage', args=['testChatName'])
        self.assertEqual(resolve(url).func, clientMessage)

    def testUrlClientCreateComprobateChat(self):
        url = reverse('clientCreateComprobateChat', args=['testUsername'])
        self.assertEqual(resolve(url).func, clientCreateComprobateChat)

    def testUrlFreelancerCreateComprobateChat(self):
        url = reverse('freelancerCreateComprobateChat', args=['testUsername'])
        self.assertEqual(resolve(url).func, freelancerCreateComprobateChat)