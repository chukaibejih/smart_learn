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
        
        

class SMSCodeModelTestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(

            username='testuser',

            email='testuser@test.com',

            password='testpass'

        )

        self.sms_code = SMSCode.objects.create(

            user=self.user,

            number='123456'

        )

    def test_sms_code_str(self):

        expected = f'{self.user.username}-123456'

        self.assertEqual(str(self.sms_code), expected)

    def test_sms_code_number_generated(self):

        self.assertEqual(len(self.sms_code.number), 6)

    def test_sms_code_is_expired(self):

        # Verify that SMS code is not expired yet

        self.assertFalse(self.sms_code.is_expired())

        # Set created_at to more than 10 minutes ago

        self.sms_code.created_at = timezone.now() - timezone.timedelta(minutes=11)

        self.sms_code.save()

        # Verify that SMS code is expired

        self.assertTrue(self.sms_code.is_expired())

    def test_create_sms_code(self):

        url = reverse('sms_code')

        self.client = APIClient()

        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(SMSCode.objects.count(), 2)

    def test_create_sms_code_without_auth(self):

        url = reverse('sms_code')

        self.client = APIClient()

        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(SMSCode.objects.count(), 1)
