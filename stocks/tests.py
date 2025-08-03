from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Stock


class SymbolFetchTests(APITestCase):
    # set up the authentication first 
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass111', email='test@gmail.com')
        # get teh token
        token_response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass111'
        })
        self.token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Create a test stock
        self.existing_stock = Stock.objects.create(
            symbol='AAPL',
            company_name='Apple Inc.',
            last_price=150.0
        )
        
    def test_fetch_by_symbol(self):
        url = reverse('fetch-by-symbol') + '?symbol=TSLA'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_fetch_existing_stock(self):
        url = reverse('fetch-by-symbol') + '?symbol=AAPL'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['symbol'], 'AAPL')

    def test_missing_symbol(self):
        url = reverse('fetch-by-symbol')  # No symbol parameter
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)