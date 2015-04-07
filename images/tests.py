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

        self.user2 = Account.objects.create_user(email="imag2e@kehko.com", username='image2', password='pwd')

        #set up couple of companies
        self.companyOne = Company.objects.create(company_name="Image abc", account_owner=self.user)
        self.companyTwo = Company.objects.create(company_name="Image abcd", account_owner=self.user2)

    def test_image_upload_and_list(self):
        client = APIClient()
        test_image_filename = os.path.join('/home/jaakko', 'Desktop', 'test.jpg')

        with open(test_image_filename, 'rb') as image_file:
            data = {
                    'name': 'test_image',
                    'image': image_file,
                    }
            #as anauthenticated
            response = client.post('/api/v1/images/', data)
            self.assertEqual(response.status_code, 401)

        with open(test_image_filename, 'rb') as image_file:
            data = {
                    'name': 'test_image',
                    'image': image_file,
                    }
            #as authenticated user
            client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
            response = client.post('/api/v1/images/', data)
            self.assertEqual(response.status_code, 201)

        #now add company accounts, add wrong account
        with open(test_image_filename, 'rb') as image_file:
            data = {
                    'name': 'test_image',
                    'image': image_file,
                    }
            data['company'] = self.companyTwo.pk
            response = client.post('/api/v1/images/', data)
            self.assertEqual(response.status_code, 403)

        #now add the correct company pk
        with open(test_image_filename, 'rb') as image_file:
            data = {
                    'name': 'test_image',
                    'image': image_file,
                    }
            data['company'] = self.companyOne.pk
            response = client.post('/api/v1/images/', data)
            self.assertEqual(response.status_code, 201)

        client.credentials()
        response = client.get('/api/v1/images/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data[0]['image'].startswith("http://kehko-dev.s3.amazonaws.com"))
