from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework_jwt.views import obtain_jwt_token

from authentication.models import Account
from news.models import News
from companies.models import Company


class TestNews(APITestCase):
    def setUp(self):
        factory = APIRequestFactory()

        #set up normal user and token
        self.userOne = Account.objects.create_user(email="test@kehko.com", username="test", password="pwd")
        request = factory.post('/api/v1/auth/login/', {'email': 'test@kehko.com', 'password': 'pwd'})
        response = obtain_jwt_token(request)
        self.tokenOne = response.data['token']

        #set up normal user and token
        self.userTwo = Account.objects.create_user(email="test2@kehko.com", username="test2", password="pwd")
        request = factory.post('/api/v1/auth/login/', {'email': 'test2@kehko.com', 'password': 'pwd'})
        response = obtain_jwt_token(request)
        self.tokenTwo = response.data['token']

        #set up couple of companies
        self.companyOne = Company.objects.create(account_owner=self.userOne, company_name="One")
        self.companyTwo = Company.objects.create(account_owner=self.userTwo, company_name="Two")

    def test_create_and_list_news(self):
        client = APIClient()

        data = {'company': self.companyOne.pk,'author': self.userOne.pk, 'title': 'Chickens', 'body': 'Eat chicken'}
        #try to create as non-logged in user
        response = client.post('/api/v1/news/', data)
        self.assertEqual(response.status_code, 401)

        #create as logged in user, but as the owner of wrong accoung
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.tokenTwo)
        response = client.post('/api/v1/news/', data)
        self.assertEqual(response.status_code, 403)

        #no log in as the account owner
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.tokenOne)
        response = client.post('/api/v1/news/', data)
        self.assertEqual(response.status_code, 201)

        #create another one post
        data = {'company': self.companyOne.pk, 'title': 'Foxes', 'body': 'What does the fox say?'}
        response = client.post('/api/v1/news/', data)
        self.assertEqual(response.status_code, 201)

        #create another news for the other company
        data = {'company': self.companyTwo.pk, 'title': 'Cats',
                'body': 'What does the cat say?', 'author': self.userTwo.pk}
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.tokenTwo)
        response = client.post('/api/v1/news/', data)
        self.assertEqual(response.status_code, 201)

        #now list the news and make sure there's three of them
        client.credentials()
        response = client.get('/api/v1/news/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['title'], 'Chickens')
        self.assertEqual(response.data[1]['company'], 1)
        self.assertEqual(response.data[2]['company'], 2)
        self.assertEqual(response.data[2]['title'], "Cats")
