from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user_service.models import User, SMSCode

class UserServiceTestCase(APITestCase):

    def setUp(self):
            User.objects.create_user(
            email='test@test.com',
            first_name='John',
            last_name='Doe',
            password='testpassword',
            is_instructor = False,
            is_verified=True 
        )

    # Test registering a new user
    def test_register_user(self):
        url = reverse('register')
        data = {
            'email': 'test2@test.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'testpassword',
            'is_instructor':True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    # Test registering a user with an email that already exists in the database
    def test_register_user_with_existing_email(self):
        url = reverse('register')
        data = {
            'email': 'test@test.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'password': 'testpassword',
            'is_instructor':False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    # Test registering a user with a weak password
    def test_register_user_with_weak_password(self):
        url = reverse('register')
        data = {
            'email': 'test@test.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'weak',
            'is_instructor':False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_login_existing_user(self):
        url = reverse('token-obtain-pair')
        data = {
            'email': 'test@test.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)
