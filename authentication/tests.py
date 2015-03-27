from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import status

from authentication.models import Account
from authentication.views import AccountDetail, AccountList

# Create your tests here.
class TestLogin(APITestCase):
    def setUp(self):
        factory = APIRequestFactory()
        #set up super_token
        self.super_user = Account.objects.create_superuser(email="man@e.com", username="manne", password="man")
        request = factory.post('/api/v1/auth/login/', {'email': 'man@e.com', 'password': 'man'})
        response = obtain_jwt_token(request)
        self.super_token = response.data['token']

        #set up normal user and token
        self.normal_user = Account.objects.create_superuser(email="user@kehko.com", username="useri", password="man")
        request = factory.post('/api/v1/auth/login/', {'email': 'user@kehko.com', 'password': 'man'})
        response = obtain_jwt_token(request)
        self.normal_token = response.data['token']

    def test_login(self):
        #success case
        factory = APIRequestFactory()
        request = factory.post('/api/v1/auth/login/', {'email': 'man@e.com', 'password': 'man'})
        response = obtain_jwt_token(request)
        self.assertTrue('token' in response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #check that token is more or less in correct form
        #the token is set up in three parts, separeted by comma: 123.456.789
        token = response.data['token']
        self.assertEqual(3, len(token.split('.')))

        #fail case
        request = factory.post('/api/v1/auth/login/', {'email': 'man@e.com', 'password': 'wrong'})
        response = obtain_jwt_token(request)
        self.assertTrue('non_field_errors' in response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestAccountList(APITestCase):
    def setUp(self):
        factory = APIRequestFactory()
        #set up super_token
        self.super_user = Account.objects.create_superuser(email="man@e.com", username="manne", password="man")
        request = factory.post('/api/v1/auth/login/', {'email': 'man@e.com', 'password': 'man'})
        response = obtain_jwt_token(request)
        self.super_token = response.data['token']

        #set up normal user and token
        self.normal_user = Account.objects.create_user(email="user@kehko.com", username="useri", password="man")
        request = factory.post('/api/v1/auth/login/', {'email': 'user@kehko.com', 'password': 'man'})
        response = obtain_jwt_token(request)
        self.normal_token = response.data['token']

    def test_add_user(self):
        """
        everyone can create a new user
        """

        factory = APIRequestFactory()
        view = AccountList.as_view()
        ok_request = factory.post('/api/v1/users/', {'email': "new@kehko.com",
                                                  'username': "newkehko", 'password': 'pass'})
        response = view(ok_request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #now incomplete data
        bad_request = factory.post('/api/v1/users/', {'email': "new@kehko.com",'password': 'pass'})
        response = view(bad_request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #now wrong email
        bad_email_request = factory.post('/api/v1/users/', {'email': "newkehko.com",
                                                  'username': "newkehko", 'password': 'pass'})
        response = view(bad_email_request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_users(self):
        #only authenticated admin user should be able to see the user listing
        factory = APIRequestFactory()
        view = AccountList.as_view()

        #unauthenticated
        unauth_req = factory.get('/api/v1/users/')
        response = view(unauth_req)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        #authenticated but not admin
        user = self.normal_user
        auth_request = factory.get('/api/v1/users/')
        force_authenticate(auth_request, user=user, token=self.normal_token)
        response = view(auth_request)
        self.assertEquals(response.status_code, 403)

        #authenticated admin -> OK
        user = self.super_user
        auth_request = factory.get('/api/v1/users/')
        force_authenticate(auth_request, user=user, token=self.super_token)
        response = view(auth_request)
        #check that the id of the list's first item if 1
        self.assertTrue(response.data[0]['id']==1)
        self.assertEquals(response.status_code, 200)

class TestAccoundDetail(APITestCase):
