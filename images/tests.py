import os

from django.core.files import File
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from rest_framework_jwt.views import obtain_jwt_token

from authentication.models import Account
from companies.models import Company
from images.models import Image

class TestImages(APITestCase):
    def setUp(self):
        factory = APIRequestFactory()

        #set up a user
        self.user = Account.objects.create_user(email="image@kehko.com", username='image', password='pwd')
        request = factory.post('/api/v1/auth/login/', {'email': 'image@kehko.com', 'password': 'pwd'})
        response = obtain_jwt_token(request)
        self.token = response.data['token']

    def test_image_upload_and_list(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

        test_image_filename = os.path.join('/home/jaakko', 'Desktop', 'test.jpg')
        with open(test_image_filename, 'rb') as image_file:
            data = {
                    'name': 'test_image',
                    'image': image_file,
                    }
            response = client.post('/api/v1/images/', data)
            self.assertEqual(response.status_code, 201)

        client.credentials()
        response = client.get('/api/v1/images/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 200)