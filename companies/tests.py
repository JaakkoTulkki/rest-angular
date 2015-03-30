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

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        data = {'full_name': 'Test Company', 'slug': 'test-company'}
        response = client.post('/api/v1/companies/', data)
        self.assertEqual(response.status_code, 201)
        self.company = Company.objects.get(full_name="Test Company")
        #another company
        data = {'full_name': 'Mokia', 'slug': 'mokia'}
        response = client.post('/api/v1/companies/', data)
        self.assertEqual(response.status_code, 201)
        self.company = Company.objects.get(full_name="Mokia")

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
        self.assertEqual(response.data[-1]['full_name'], "Corp")

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
        client = APIClient()
        data = {'name': "Soap", 'slug': 'soap', 'description': "Keeps you clean",
                'price': 100}

        #try to create the product as normal user
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = client.post('/api/v1/products/test-company/', data)
        self.assertEqual(response.status_code, 403)
        client.credentials()

        #create  as admin
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        response = client.post('/api/v1/products/test-company/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['slug'], 'soap')
        self.assertEqual(response.data['owner']['full_name'], 'Test Company')

        #create another product
        data = {'name': "Cheese", 'slug': 'cheese', 'description': "This is foo",
                'price': 10}
        response = client.post('/api/v1/products/test-company/', data)
        self.assertEqual(response.status_code, 201)

        #a product for Mokia
        data = {'name': "Cheese", 'slug': 'mokia-cheese', 'description': "This is foo",
                'price': 10}
        response = client.post('/api/v1/products/mokia/', data)
        self.assertEqual(response.status_code, 201)

        #now list those products for Test Company
        client.credentials()
        response = client.get('/api/v1/products/test-company/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Soap')
        self.assertEqual(response.data[1]['name'], 'Cheese')
        self.assertEqual(response.data[0]['owner']['full_name'], 'Test Company')

        #Now list Mokia products
        response = client.get('/api/v1/products/mokia/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['owner']['full_name'], 'Mokia')


        #let's update some product
        data = {'name': "Cheese", 'slug': 'cheese', 'description': "This is food and it's good",
                'price': 12}

        #first as not admin
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = client.put('/api/v1/products/test-company/cheese/', data)
        self.assertEqual(response.status_code, 403)

        #now let's update some product as asdmin
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        response = client.put('/api/v1/products/test-company/cheese/', data)
        self.assertEqual(response.status_code, 202)
        product = Product.objects.get(slug='cheese')
        self.assertEqual(product.description, "This is food and it's good")
        self.assertEqual(product.price, 12)

        #now let's delete that product
        response = client.delete('/api/v1/products/test-company/cheese/')
        self.assertEqual(response.status_code, 204)
        product = Product.objects.filter(owner__slug="test-company", slug="cheese")
        self.assertFalse(product.exists())

