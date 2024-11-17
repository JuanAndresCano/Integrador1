from django.test import TestCase
from django.test import Client as TestClient
from django.urls import reverse
from apps.accounts.models import Userk
from django.core import mail

class TestRecoverMyAccount(TestCase):

    def setUp(self):
        self.client = TestClient()
        self.landPage = reverse('recoverPassword')
        self.passwordResetDone = reverse('password_reset_done')
        self.passwordResetConfirm = reverse('password_reset_confirm', kwargs={'uidb64': 'testuid', 'token': 'testtoken'})
        self.passwordResetComplete = reverse('password_reset_complete')
        self.user = Userk.objects.create_user(username='testuser', email='testuser@example.com', password='password123')

    def testRecoverPasswordPageAccess(self):
        """Test access to the password recovery page."""
        response = self.client.get(self.landPage)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/recoverPassword.html')

    def testRecoverPasswordSentPageAccess(self):
        """Test access to the password recovery sent page."""
        response = self.client.get(self.passwordResetDone)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/recoverPasswordSent.html')

    def testRecoverPasswordEmailSent(self):
        """Test that email is sent after requesting password reset."""
        response = self.client.post(self.landPage, {'email': 'testuser@example.com'})
        self.assertEqual(response.status_code, 302)  # Redirect after sending email
        self.assertRedirects(response, self.passwordResetDone)
        self.assertEqual(len(mail.outbox), 1)  # Check that one email has been sent
        self.assertIn('Password reset', mail.outbox[0].subject)

    def testPasswordResetConfirmPageAccess(self):
        """Test access to the password reset confirm page."""
        response = self.client.get(self.passwordResetConfirm)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/recoverPasswordForm.html')

    def testPasswordResetCompletePageAccess(self):
        """Test access to the password reset complete page."""
        response = self.client.get(self.passwordResetComplete)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/recoverPasswordDone.html')

    def testValidPasswordReset(self):
        """Test the full password reset process."""
        # Simula la solicitud de recuperación de contraseña
        response = self.client.post(self.landPage, {'email': 'testuser@example.com'})
        
        # Asegúrate de que el correo electrónico de restablecimiento se haya enviado
        self.assertEqual(len(mail.outbox), 1)
        resetEmail = mail.outbox[0]
        
        # Extrae el enlace de restablecimiento de la contraseña del cuerpo del correo
        resetLink = None
        for line in resetEmail.body.splitlines():
            if "http" in line:
                resetLink = line
                break

        # Asegúrate de que el enlace de restablecimiento de contraseña se haya encontrado
        self.assertIsNotNone(resetLink)
        
        # Divide el enlace para obtener el uidb64 y el token
        # El enlace debería tener el formato 'http://localhost:8000/recover/<uidb64>/<token>'
        path = resetLink.split('/')[-2:]  # Esto debería darte [uidb64, token]
        
        if len(path) != 2:
            self.fail("No se pudieron extraer correctamente el uidb64 y el token del enlace")

        uidb64, token = path
        
        # Simula el restablecimiento de la contraseña con el token
        resetUrl = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
        response = self.client.post(resetUrl, {'new_password1': 'password123', 'new_password2': 'password123'})
        
        self.assertEqual(response.status_code, 302)  # Redirección después de restablecer la contraseña

        # Verifica que el usuario pueda iniciar sesión con la nueva contraseña
        user = Userk.objects.get(username='testuser')
        self.assertTrue(user.check_password('password123'))  # La validación debería pasar correctamente
