from django.test import TestCase
from django.urls import reverse
from apps.accounts.models import Client, Userk

class ClientRegisterTests(TestCase):

    def setUp(self):
        self.client_register_url = reverse('clientRegister')  # Asegúrate de que el nombre coincida
        self.valid_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123',
            'phoneNumber': '123456789',
            'taxId': 'TAX12345',
            'companyName': 'Test Company',
            'typeOfCompany': 'SaaS',
            'businessVertical': 'Software',
            'country': 'US',
            'city': 'New York',
            'address': '123 Test Street'
        }

    def testClientRegisterPageLoads(self):
        """
        Verifica que la página de registro de cliente carga correctamente.
        """
        response = self.client.get(self.client_register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/clientRegister.html')

    def testClientRegisterValidPost(self):
        """
        Prueba que un cliente válido se registre correctamente y se cree un objeto Client.
        """
        response = self.client.post(self.client_register_url, self.valid_data)
        
        # Asegurarse de que el usuario y el cliente se hayan creado
        self.assertEqual(Userk.objects.count(), 1)
        self.assertEqual(Client.objects.count(), 1)
        
        # Comprobar redirección (suponiendo que rediriges a otra página tras el registro)
        self.assertEqual(response.status_code, 302)

        # Comprobar que los datos del cliente son correctos
        client = Client.objects.first()
        self.assertEqual(client.user.username, 'testuser')
        self.assertEqual(client.phoneNumber, '123456789')
        self.assertEqual(client.companyName, 'Test Company')

    def testClientRegisterInvalidPost(self):
        """
        Verifica que los errores de validación se gestionen correctamente.
        Por ejemplo, contraseñas que no coinciden.
        """
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'WrongPassword'
        
        response = self.client.post(self.client_register_url, invalid_data)
        
        # No se debería haber creado ningún usuario ni cliente
        self.assertEqual(Userk.objects.count(), 0)
        self.assertEqual(Client.objects.count(), 0)
        
        # La respuesta debería mostrar errores en el formulario
        self.assertEqual(response.status_code, 200)  # Se debería quedar en la misma página con los errores
        self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')

    def testRequiredFields(self):
        """
        Verifica que todos los campos requeridos se gestionen correctamente.
        """
        required_fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phoneNumber', 'taxId', 'companyName', 'typeOfCompany', 'businessVertical', 'country', 'city', 'address']
        
        for field in required_fields:
            data = self.valid_data.copy()
            data[field] = ''  # Eliminar el campo requerido
            
            response = self.client.post(self.client_register_url, data)
            
            self.assertEqual(response.status_code, 200)  # Se queda en la página mostrando el error
            self.assertFormError(response, 'form', field, 'This field is required.')

