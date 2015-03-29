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
        self.cause_man = Account.objects.create_user(email="causeman@kehko.com", username="causeman", password="pwd")
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
        #creator', 'name', 'sponsors', 'slug', 'description', 'likes', 'followers', 'members
        data = {'name': 'NWO', 'slug': 'nwo', 'description': 'NWO awaits!!'}
        response = client.post('/api/v1/causes/', data)
        self.assertEqual(response.status_code, 403)

        #now we are superuser -> should be able to create
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        data = {'name': 'NWO', 'slug': 'nwo', 'description': 'NWO awaits!!'}
        #data['creator'] = {"username":["supercause"],"email":["supercause@kehko.com"]}
        response = client.post('/api/v1/causes/', data)
        #print(response.__dir__())
        print(response.serialize())
        self.assertEqual(response.status_code, 201)