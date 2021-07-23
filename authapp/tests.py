from django.conf import settings
from django.test import TestCase
from django.test.client import Client

from authapp.models import ShopUser


class UserManagementTestCase(TestCase):
    status_code_success = 200
    status_code_redirect = 302

    username = 'django'
    email = 'django@gb.local'
    password = 'geekbrains'

    new_user_data = {
        'username': 'django1',
        'first_name': 'django1',
        'last_name': 'django1',
        'password1': 'geekbrains',
        'password2': 'geekbrains',
        'email': 'django@gb.local',
        'age': 33,
    }

    def setUp(self):
        self.user = ShopUser.objects.create_superuser(username=self.username, email=self.email,
                                                      password=self.password)
        self.client = Client()

    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertTrue(response.context['user'].is_anonymous)

        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/auth/login/')
        print(response.status_code)
        self.assertEqual(response.status_code, self.status_code_redirect)

    def test_user_register(self):
        new_user_data = {
            'username': 'django1',
            'first_name': 'django1',
            'last_name': 'django1',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'django@gb.local',
            'age': 33,
        }

        response = self.client.post('/auth/user/register/', data=self.new_user_data)
        self.assertEqual(response.status_code, self.status_code_redirect)

        new_user = ShopUser.objects.get(username=self.new_user_data['username'])

        activation_url = f"{settings.DOMAIN_NAME}/auth/user/verify/{new_user_data['email']}/{new_user.activation_key}/"
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, self.status_code_success)

        new_user.refresh_from_db()
        self.assertTrue(new_user.is_active)
