import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient, APIRequestFactory, APITestCase, force_authenticate
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import status


from authentication.models import Account
from authentication.views import AccountDetail, AccountList
from causes.models import Cause
from companies.models import Company, Product

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

        #create random normal user
        ac = Account.objects.create(email="random@kehko.com", username="randomkehko", password="pwd")

    def test_add_user(self):
        """
        everyone can create a new user
        """
        factory = APIRequestFactory()
        view = AccountList.as_view()
        dob = datetime.datetime.now() - datetime.timedelta(days=365)
        #datetime.datetime.strftime(dob, "%c")
        #dob = datetime.date.isoformat(dob)
        data = {'email': "anew@kehko.com", 'username': "kana",
                'password': 'pass', 'date_of_birth': datetime.date(2015, 1, 1)}
        ok_request = factory.post('/api/v1/users/', data)
        response = view(ok_request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['date_of_birth'], datetime.date(2015, 1, 1))

        #now incomplete data
        bad_request = factory.post('/api/v1/users/', {'email': "new@kehko.com", 'password': 'pass'})
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
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

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

        #check that you are able to get only certain accouts using pks
        auth_request = factory.get('/api/v1/users/?ids=1,3')
        force_authenticate(auth_request, user=user, token=self.super_token)
        response = view(auth_request)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(sorted([e['id'] for e in response.data]), [1, 3])


class TestAccountDetail(APITestCase):
    def setUp(self):
        factory = APIRequestFactory()
        #set up normal user and token
        self.normal_user = Account.objects.create_user(email="user@kehko.com", username="accountDetail", password="man")
        request = factory.post('/api/v1/auth/login/', {'email': 'user@kehko.com', 'password': 'man'})
        response = obtain_jwt_token(request)
        self.normal_token = response.data['token']

        self.user2 = Account.objects.create_user(email="user2@kehko.com", username="hello", password="man")
        request = factory.post('/api/v1/auth/login/', {'email': 'user2@kehko.com', 'password': 'man'})
        response = obtain_jwt_token(request)
        self.token2 = response.data['token']

        self.user3 = Account.objects.create_user(email="user3@kehko.com", username="user3", password="man")
        self.user4 = Account.objects.create_user(email="user4@kehko.com", username="user4", password="man")

        #create couple of companies
        self.companyOne = Company.objects.create(account_owner=self.normal_user, company_name="xyz")
        self.companyTwo = Company.objects.create(account_owner=self.user2, company_name="abc")

        #a product for companyOne
        self.productOne = Product.objects.create(owner=self.companyOne, name='chicken',
                                                 description="tastes good", price=3.4)


    def test_details(self):
        """
        tests whether you can see account details
        only authenticated user should get this data
        :return:
        """

        #unauthenticated
        client = APIClient()
        response = client.get('/api/v1/users/accountDetail/')
        self.assertEqual(response.status_code, 401)

        #authenticated but, not account ownger
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token2)
        response = client.get('/api/v1/users/accountDetail/')
        self.assertEqual(response.status_code, 403)
        client.credentials()

        #authenticated and the account owner
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.normal_token)
        response = client.get('/api/v1/users/accountDetail/')
        self.assertEqual(response.status_code, 200)

    def test_update_account(self):
        """
        try to test whether you can update your account
        :return:
        """
        data = {'first_name': 'Fname', 'last_name': 'Lname', 'tagline': 'Life', 'password': 'man'}
        #wrong account, user2 tries to update normal users's account
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token2)
        response = client.put('/api/v1/users/accountDetail/', data)
        self.assertEqual(response.status_code, 403)

        #right account, normal user trie to update but with missing data
        data = {'first_name': 'Fname', 'last_name': 'Lname', 'tagline': 'Life', }
        user = self.normal_user
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.normal_token)
        response = client.put('/api/v1/users/accountDetail/', data)
        self.assertEqual(response.status_code, 403)

        #right account, normal user updates with complete data, add also couple of followers
        user_pks = [self.user3.pk, self.user4.pk]
        company_pks = [self.companyOne.pk, self.companyTwo.pk]
        data = {'first_name': 'Fname', 'last_name': 'Lname', 'tagline': 'Life', 'password': 'man',
                'followees': user_pks, 'liked_companies': company_pks,
                'liked_products': [self.productOne.pk], 'date_of_birth': datetime.date(2010, 10, 22)}
        user = self.normal_user
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.normal_token)
        response = client.put('/api/v1/users/accountDetail/', data)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data['liked_companies'], company_pks)
        self.assertEqual(response.data['liked_products'], [self.productOne.pk])
        self.assertEqual(response.data['date_of_birth'], '2010-10-22')

        #make sure that the stuff was updated
        response = client.get('/api/v1/users/accountDetail/')
        self.assertEqual(response.data['tagline'], 'Life')
        self.assertEqual(response.data['followees'], user_pks)
        self.assertEqual(len(self.user3.account_set.all()), 1)
        self.assertEqual(self.normal_user.liked_products.all()[0], self.productOne)

class TestListCausesForUser(APITestCase):
    def setUp(self):
        #create user
        self.user = Account.objects.create_superuser(email="abc@kehko.com", username="abc", password='abc')

        #create second user
        self.user2 = Account.objects.create_superuser(email="def@kehko.com", username="def", password='abc')


    def test_listing_causes(self):
        cause1 = Cause.objects.create(name="cause1", description="desc", creator=self.user)
        cause1.save()
        cause2 = Cause.objects.create(name="cause2", description="desc", creator=self.user2)
        cause2.save()
        cause2.followers.add(self.user)
        cause2.save()

        #now self.user is a member in two causes: the one he created and then as a follower in cause2

        client = APIClient()
        response = client.get('/api/v1/users/{}/causes/'.format('abc'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

