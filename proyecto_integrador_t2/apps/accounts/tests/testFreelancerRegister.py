from django.test import TestCase
from django.urls import reverse
from apps.accounts.models import Freelancer, Userk
from apps.accounts.forms import SignUpFormFreelancer
class FreelancerRegisterTests(TestCase):
    def setUp(self):
        self.freelancer_register_url = reverse('freelancerRegister')  # Asegúrate de que el nombre coincida
        self.valid_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'TestPass123#',
            'password2': 'TestPass123#',
            'phoneNumber': '123456789',
            'identification': '1005967728',
        }
    def testFreelancerRegisterPageLoads(self):
        """
        Verifica que la página de registro de freelancer carga correctamente.
        """
        response = self.client.get(self.freelancer_register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/freelancerRegister.html')
        self.assertTrue(isinstance(response.context['form'], SignUpFormFreelancer))
    def testFreelancerRegisterValidPost(self):
        """
        Prueba que un freelancer válido se registre correctamente y se cree un objeto freelancer.
        """
        response = self.client.post(self.freelancer_register_url, self.valid_data)
        
        # Asegurarse de que el usuario y el cliente se hayan creado
        self.assertEqual(Userk.objects.count(), 1)
        self.assertEqual(Freelancer.objects.count(), 1)
        
        # Comprobar redirección (suponiendo redirección a otra página tras el registro)
        self.assertEqual(response.status_code, 302)
        # Comprobar que los datos del cliente son correctos
        freelancer = Freelancer.objects.first()
        self.assertEqual(freelancer.user.username, self.valid_data['username'])
        self.assertEqual(freelancer.user.first_name, self.valid_data['first_name'])
        self.assertEqual(freelancer.user.last_name, self.valid_data['last_name'])
        self.assertEqual(freelancer.user.email, self.valid_data['email'])
        self.assertEqual(freelancer.phoneNumber, self.valid_data['phoneNumber'])
        self.assertEqual(freelancer.identification, self.valid_data['identification'])
        self.assertTrue(freelancer.user.is_freelancer)
    def testFreelancerRegisterInvalidPasswordPost(self):
        """
        Verifica que los errores de validación se gestionen correctamente.
        Por ejemplo, contraseñas que no coinciden.
        """
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'WrongPassword'
        
        response = self.client.post(self.freelancer_register_url, invalid_data)
        
        # No se debería haber creado ningún usuario ni cliente
        self.assertEqual(Userk.objects.count(), 0)
        self.assertEqual(Freelancer.objects.count(), 0)
        
        # La respuesta debería mostrar errores en el formulario
        self.assertEqual(response.status_code, 200)  # Se debería quedar en la misma página con los errores
        self.assertTemplateUsed(response, 'accounts/freelancerRegister.html')