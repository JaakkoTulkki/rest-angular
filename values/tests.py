from rest_framework.test import APIClient,APIRequestFactory, APITestCase, force_authenticate
from rest_framework_jwt.views import obtain_jwt_token

from authentication.models import Account
from values.models import Value

class TestValues(APITestCase):
    def setUp(self):
        factory = APIRequestFactory()

        #set up normal user and token
        self.normal_user = Account.objects.create_user(email="values@kehko.com", username="values", password="pwd")
        request = factory.post('/api/v1/auth/login/', {'email': 'values@kehko.com', 'password': 'pwd'})
        response = obtain_jwt_token(request)
        self.token = response.data['token']

        #set up admin user
        self.cause_man = Account.objects.create_superuser(email="supervalues@kehko.com", username="supervalue",
                                                          password="pwd")
        request = factory.post('/api/v1/auth/login/', {'email': 'supervalues@kehko.com', 'password': 'pwd'})
        response = obtain_jwt_token(request)
        self.super_token = response.data['token']

    def test_list_values(self):
        client = APIClient()

        data = {'name':'Freedom', 'description': "We all want freedom"}

        #try to create as non authenticated
        response = client.post('/api/v1/values/', data)
        self.assertEqual(response.status_code, 401)
        self.assertFalse(Value.objects.all().exists())

        #create a value as authenticated
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = client.post('/api/v1/values/', data)
        self.assertEqual(response.status_code, 201)

        #create another value
        data = {'name': 'Health', 'description': "Take care"}
        response = client.post('/api/v1/values/', data)
        self.assertEqual(response.status_code, 201)

        #list values as non-authenticated
        client.credentials()
        response = client.get('/api/v1/values/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[1]['name'], 'Health')

        slug1 = response.data[0]['slug']
        slug2 = response.data[1]['slug']

        #get details
        response = client.get('/api/v1/values/{}/'.format(slug1))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['slug'], slug1)
        self.assertEqual(response.data['name'], 'Freedom')

        response = client.get('/api/v1/values/{}/'.format(slug2))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['slug'], slug2)
        self.assertEqual(response.data['name'], 'Health')

        #try to update or delete as normal user
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = client.delete('/api/v1/values/{}/'.format(slug1))
        self.assertEqual(response.status_code, 403)

        data = {'name': 'Freedom!!'}
        response = client.put('/api/v1/values/{}/'.format(slug1), data)
        self.assertEqual(response.status_code, 403)

        #now update and delete as admin
        client.credentials()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        response = client.put('/api/v1/values/{}/'.format(slug1), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Value.objects.get(slug=slug1).name, data['name'])

        response = client.delete('/api/v1/values/{}/'.format(slug1))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Value.objects.filter(slug=slug1).exists())