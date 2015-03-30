from rest_framework.test import APIClient,APIRequestFactory, APITestCase, force_authenticate
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import status

from authentication.models import Account
from companies.models import Company, Product
from companies.serializers import CompanySerializer, ProductSerializer


class TestCause(APITestCase):
    def setUp(self):
        factory = APIRequestFactory()

        #set up normal user and token
        self.normal_user = Account.objects.create_user(email="company@kehko.com", username="company", password="pwd")
        request = factory.post('/api/v1/auth/login/', {'email': 'company@kehko.com', 'password': 'pwd'})
        response = obtain_jwt_token(request)
        self.token = response.data['token']

        #set up admin user
        self.cause_man = Account.objects.create_superuser(email="supercompany@kehko.com", username="supercompany",
                                                          password="pwd")
        request = factory.post('/api/v1/auth/login/', {'email': 'supercompany@kehko.com', 'password': 'pwd'})
        response = obtain_jwt_token(request)
        self.super_token = response.data['token']

    def test_company(self):
        client = APIClient()

        #try to create a company, not admin
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        data = {'full_name': 'Corp', 'slug': 'corp'}
        response = client.post('/api/v1/companies/', data)
        self.assertEqual(response.status_code, 403)
        client.credentials()

        #now admin -> should work
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        data = {'full_name': 'Corp', 'slug': 'corp'}
        response = client.post('/api/v1/companies/', data)
        self.assertEqual(response.status_code, 201)

        company = Company.objects.get(full_name="Corp")
        self.assertEqual(company.full_name, "Corp")

        #make sure that non authenticated users can see the list of companies
        client.credentials()
        response = client.get('/api/v1/companies/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['full_name'], "Corp")

        #now try to retrieve the company info from CompanyDetail view
        response = client.get('/api/v1/companies/corp/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['full_name'], "Corp")

        #try to update as normal user
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        data = {'full_name': 'Corp Ltd.', 'slug': 'corp-ltd'}
        response = client.put('/api/v1/companies/corp/', data)
        self.assertEqual(response.status_code, 403)

        #now update as admin user
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        data = {'full_name': 'Corp Ltd.', 'slug': 'corp-ltd'}
        response = client.put('/api/v1/companies/corp/', data)
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data['full_name'], "Corp Ltd.")

        #now the old stuff should have disappeared
        response = client.get('/api/v1/companies/corp/')
        self.assertEqual(response.status_code, 404)

        #and the new slug should work -> retrieve
        response = client.get('/api/v1/companies/corp-ltd/')
        self.assertEqual(response.status_code, 200)

        #try to delete as normal user
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = client.delete('/api/v1/companies/corp-ltd/')
        self.assertEqual(response.status_code, 403)

        #now delete as admin
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        response = client.delete('/api/v1/companies/corp-ltd/')
        self.assertEqual(response.status_code, 204)

        #and make sure that it's gone
        company = Company.objects.filter(slug="corp-ltd")
        self.assertFalse(company.exists())

    def test_product(self):
        pass
