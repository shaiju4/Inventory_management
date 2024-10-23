from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

class LoginViewTests(APITestCase):
    
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        User.objects.create_user(username=self.username, password=self.password)
        self.url = reverse('login')  

    def test_login_success(self):
        response = self.client.post(self.url, {
            'username': self.username,
            'password': self.password
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data['data'])
        self.assertIn('refresh', response.data['data'])

    def test_login_invalid_credentials(self):
        response = self.client.post(self.url, {
            'username': self.username,
            'password': 'wrongpassword'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], "Login Failed")
