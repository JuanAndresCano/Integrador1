from django.test import SimpleTestCase
from django.urls import reverse, resolve
from apps.accounts.views import *
from django.contrib.auth import views as auth_views

class TestUrls(SimpleTestCase):

    
    def testUrlLogin(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, loginPage)

    def testUrlLandpage(self):
        url = reverse('landpage')
        self.assertEqual(resolve(url).func, landpage)

    def testUrlFreelancerRegister(self):
        url = reverse('freelancerRegister')
        self.assertEqual(resolve(url).func, freelancerRegister)

    def testUrlClientRegister(self):
        url = reverse('clientRegister')
        self.assertEqual(resolve(url).func, clientRegister)

    def testUrlLogout(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, logout)

    def testUrlClientProfile(self):
        url = reverse('clientProfile')
        self.assertEqual(resolve(url).func, client_profile)

    def testUrlFreelancerProfile(self):
        url = reverse('freelancerProfile', args=[1])
        self.assertEqual(resolve(url).func, freelancer_profile)
    
    def testUrlfprofileRequest(self):
        url = reverse('fprofileRequest', args=[1, 2])
        self.assertEqual(resolve(url).func, fprofileRequest)

    def testUrlfreelancerProfileSettings(self):
        url = reverse('freelancerProfileSettings')
        self.assertEqual(resolve(url).func, freelancer_profile_settings)
    
    def test_recoverPassword_url_resolves(self):
        url = reverse('recoverPassword')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetView)

    def test_recoverPasswordSent_url_resolves(self):
        url = reverse('password_reset_done')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetDoneView)

    def test_recoverPasswordConfirm_url_resolves(self):
        # Probar la URL con ejemplos de `uidb64` y `token` como parámetros
        url = reverse('password_reset_confirm', args=['uidb64', 'token'])
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetConfirmView)

    def test_recoverPasswordDone_url_resolves(self):
        url = reverse('password_reset_complete')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetCompleteView)