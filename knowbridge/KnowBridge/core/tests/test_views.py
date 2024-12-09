from django.test import TestCase, Client
from django.urls import reverse
from core.models import CustomUser
from core.forms import CustomUserCreationForm, CustomUserLoginForm

class UserTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.home_url = reverse('home')
        

    def test_register_page(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_home_page(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_user_registration(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'identifier': '1AB12CD123',
            'user_type': 'student'
        })
        self.assertEqual(response.status_code, 302)  # Redirects to login
        self.assertTrue(CustomUser.objects.filter(email='test@example.com').exists())

    def test_user_login(self):
        user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpassword', identifier='1AB12CD123', user_type='student')
        response = self.client.post(self.login_url, {
            'identifier': '1AB12CD123',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirects to dashboard or appropriate page
