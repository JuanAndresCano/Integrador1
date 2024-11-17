from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models import Userk
from apps.accounts.forms import SignUpFormFreelancer


class testViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = Userk.objects.create_user(username='testuser', password='password123')

    def test_login_view_GET(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_invalid_user_view_POST(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
    

    def test_login_view_POST(self):
        response = self.client.post(reverse('login'), {
            'username': 'c',
            'password': 'client0105'
        })
        print(response.content)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('clientProject'))
    
    def test_signup_form_not_valid_data(self):
        form = SignUpFormFreelancer(data={
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password1': 'password123',
            'password2': 'password123',
            'identification': '123456789',
            'phoneNumber': '555-5555'
        })
        print("Is not valid cos password is too common")
        self.assertFalse(form.is_valid())

    def test_signup_form_valid_data(self):
            form = SignUpFormFreelancer(data={
                'first_name': 'John',
                'last_name': 'Doe',
                'username': 'johndoe',
                'email': 'johndoe@example.com',
                'password1': 'EySiMrJohn095',
                'password2': 'EySiMrJohn095',
                'identification': '123456789',
                'phoneNumber': '555-5555'
            })
            print("It should be valid")
            self.assertTrue(form.is_valid())
