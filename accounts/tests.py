from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class AuthTests(APITestCase):
    def test_register(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'test@gmail.com',
            'password': 'test123456',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_login(self):
        # First create a user
        User.objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='test123456'
        )
        
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'test123456'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)