from rest_framework.test import APIClient, APIRequestFactory, APITestCase, force_authenticate
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import status

from authentication.models import Account
from causes.models import CauseMembers, Cause
from causes.serializers import CauseMemberSerializer, CauseSerializer

class TestCause(APITestCase):
    def setUp(self):
        factory = APIRequestFactory()

        #set up normal user and token
        self.normal_user = Account.objects.create_user(email="causeman@kehko.com", username="causeman", password="pwd")
        request = factory.post('/api/v1/auth/login/', {'email': 'causeman@kehko.com', 'password': 'pwd'})
        response = obtain_jwt_token(request)
        self.token = response.data['token']

        #set up admin user
        self.cause_man = Account.objects.create_superuser(email="supercause@kehko.com", username="supercause", password="pwd")
        request = factory.post('/api/v1/auth/login/', {'email': 'supercause@kehko.com', 'password': 'pwd'})
        response = obtain_jwt_token(request)
        self.super_token = response.data['token']

    def test_create_cause_and_list(self):
        #we are not admin, thus not able to create cause
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        data = {'name': 'NWO', 'description': 'NWO awaits!!'}
        response = client.post('/api/v1/causes/', data)
        self.assertEqual(response.status_code, 403)

        #now we are superuser -> should be able to create
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        data = {'name': 'NWO', 'description': 'NWO awaits!!'}
        response = client.post('/api/v1/causes/', data)
        #print(response.__dir__())
        #print(response.serialize())
        self.assertEqual(response.status_code, 201)

        #now check that it was saved correctly
        cause = Cause.objects.get(name='NWO')
        self.assertEqual(cause.name, "NWO")
        self.assertEqual(cause.description, 'NWO awaits!!')
        self.assertEqual(cause.creator, self.cause_man)

        #create another cause
        data = {'name': 'Save Water', 'description': 'We are the world!'}
        response = client.post('/api/v1/causes/', data)
        self.assertEqual(response.status_code, 201)
        slug = response.data['slug']

        #check that we have two causes
        response = client.get('/api/v1/causes/')
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['creator']['username'], 'supercause')
        self.assertEqual(response.data[0]['name'], 'NWO')
        self.assertEqual(response.data[1]['name'], 'Save Water')

        #check that details work
        response = client.get('/api/v1/causes/{}/'.format(slug))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Save Water')

        #now update with falsy data
        data = {'description': ""}
        response = client.put('/api/v1/causes/{}/'.format(slug), data)
        self.assertEqual(response.status_code, 400)

        #now update the cause with correct data
        data = {'name': 'Save Water-Resources', 'description': "Where's the justice"}
        response = client.put('/api/v1/causes/{}/'.format(slug), data)
        self.assertEqual(response.status_code, 202)

        #check that the new stuff is saved and the slug is the same!!
        response = client.get('/api/v1/causes/{}/'.format(slug))
        self.assertEqual(response.status_code, 200)

        #unauthenticated should not be able to login
        client.credentials()
        data = {'name': 'Save Water-Resources', 'description': "Where's the justice"}
        response = client.put('/api/v1/causes/{}/'.format(slug), data)
        self.assertEqual(response.status_code, 401)
        #or delete
        response = client.delete('/api/v1/causes/save-water/', data)
        self.assertEqual(response.status_code, 401)

        #then try to put and delete as normal user
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = client.put('/api/v1/causes/save-water/', data)
        self.assertEqual(response.status_code, 403)
        #or delete
        response = client.delete('/api/v1/causes/save-water/', data)
        self.assertEqual(response.status_code, 403)

        #but deletion should work with admin
        client.credentials()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        response = client.delete('/api/v1/causes/{}/'.format(slug), data)
        self.assertEqual(response.status_code, 204)
        cause = Cause.objects.filter(slug=slug)
        self.assertEqual(False, cause.exists())