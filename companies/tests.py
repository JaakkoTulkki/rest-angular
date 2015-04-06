from rest_framework.test import APIClient, APIRequestFactory, APITestCase, force_authenticate
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import status

from authentication.models import Account
from causes.models import Cause
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

        #create a company
        data = {'company_name': 'Test Company'}
        response = client.post('/api/v1/companies/', data)
        self.assertEqual(response.status_code, 201)
        self.company = Company.objects.get(company_name="Test Company")
        self.test_slug = response.data['slug']
        #another company
        data = {'company_name': 'Mokia'}
        response = client.post('/api/v1/companies/', data)
        self.assertEqual(response.status_code, 201)
        self.mokia = Company.objects.get(company_name="Mokia")
        self.mokia_slug = response.data['slug']
        #third company
        data = {'company_name': 'Moke'}
        response = client.post('/api/v1/companies/', data)
        self.assertEqual(response.status_code, 201)
        self.moke = Company.objects.get(company_name="Moke")
        self.moke_slug = response.data['slug']

        #create a Cause
        self.cause = Cause.objects.create(creator=self.cause_man, name="Test cause", description="desc")

    def test_company(self):
        client = APIClient()

        #try to create a company, not admin
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        data = {'company_name': 'Corp', 'slug': 'corp'}
        response = client.post('/api/v1/companies/', data)
        self.assertEqual(response.status_code, 403)
        client.credentials()

        #now admin -> should work
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        data = {'company_name': 'Corp', 'slug': 'corp'}
        response = client.post('/api/v1/companies/', data)
        self.assertEqual(response.status_code, 201)

        company = Company.objects.get(company_name="Corp")
        self.assertEqual(company.company_name, "Corp")

        #make sure that non authenticated users can see the list of companies
        client.credentials()
        response = client.get('/api/v1/companies/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[-1]['company_name'], "Corp")

        #now try to retrieve the company info from CompanyDetail view
        response = client.get('/api/v1/companies/corp/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['company_name'], "Corp")
        slug = response.data['slug']

        #try to update as normal user
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        data = {'company_name': 'Corp Ltd.', 'slug': 'corp-ltd'}
        response = client.put('/api/v1/companies/{}/'.format(slug), data)
        self.assertEqual(response.status_code, 403)

        #now update as admin user
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        data = {'company_name': 'Corp Ltd.', 'slug': 'corp-ltd'}
        response = client.put('/api/v1/companies/{}/'.format(slug), data)
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data['company_name'], "Corp Ltd.")
        self.assertEqual(response.data['slug'], slug)

        #the slug should have stayed the same
        response = client.get('/api/v1/companies/{}/'.format(slug))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['slug'], slug)

        #try to delete as normal user
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = client.delete('/api/v1/companies/{}/'.format(slug))
        self.assertEqual(response.status_code, 403)

        #now delete as admin
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        response = client.delete('/api/v1/companies/{}/'.format(slug))
        self.assertEqual(response.status_code, 204)

        #and make sure that it's gone
        company = Company.objects.filter(slug=slug)
        self.assertFalse(company.exists())

    def test_product(self):
        client = APIClient()
        data = {'name': "Soap", 'description': "Keeps you clean",
                'price': '100'}

        #try to create the product as normal user
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = client.post('/api/v1/products/test-company/', data)
        self.assertEqual(response.status_code, 403)
        client.credentials()

        #create  as admin
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)

        response = client.post('/api/v1/products/{}/'.format(self.test_slug), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['slug'], self.test_slug+'-soap')
        self.assertEqual(response.data['owner']['company_name'], 'Test Company')

        #try to create again the same product
        response = client.post('/api/v1/products/{}/'.format(self.test_slug), data)
        self.assertEqual(response.status_code, 409)

        #create another product
        data = {'name': "Cheese",'description': "This is foo", 'price': 10}
        response = client.post('/api/v1/products/{}/'.format(self.test_slug), data)
        self.assertEqual(response.status_code, 201)

        #a product for Mokia
        data = {'name': "Cheese", 'description': "This is foo", 'price': 10}
        response = client.post('/api/v1/products/{}/'.format(self.mokia_slug), data)
        self.assertEqual(response.status_code, 201)

        #now list those products for Test Company
        client.credentials()
        response = client.get('/api/v1/products/test-company/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Soap')
        self.assertEqual(response.data[1]['name'], 'Cheese')
        self.assertEqual(response.data[0]['owner']['company_name'], 'Test Company')

        #Now list Mokia products
        response = client.get('/api/v1/products/mokia/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['owner']['company_name'], 'Mokia')


        #let's update some product
        data = {'name': "Cheese", 'slug': 'cheese', 'description': "This is food and it's good",
                'price': 12}

        #first as not admin
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = client.put('/api/v1/products/test-company/cheese/', data)
        self.assertEqual(response.status_code, 403)

        #now let's update some product as asdmin
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        response = client.put('/api/v1/products/{0}/{1}/'.format(self.test_slug, self.test_slug+'-cheese'),
                              data)
        self.assertEqual(response.status_code, 202)
        product = Product.objects.get(slug=self.test_slug+'-cheese')
        self.assertEqual(product.description, "This is food and it's good")
        self.assertEqual(product.price, 12)

        #now let's delete that product
        #but first make sure that there is this kind of product
        product = Product.objects.filter(owner__slug=self.test_slug, slug=self.test_slug+'-cheese')
        self.assertTrue(product.exists())
        #now delete
        response = client.delete('/api/v1/products/{0}/{1}/'.format(self.test_slug, self.test_slug+'-cheese'))
        self.assertEqual(response.status_code, 204)
        #and make sure that the query above return None
        product = Product.objects.filter(owner__slug=self.test_slug, slug=self.test_slug+'-cheese')
        self.assertFalse(product.exists())

    def test_company_fields(self):
        client = APIClient()
        #let's take test_company and add Moke and Mokia to its following-company
        #also add following_user
        #and following_cause
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.super_token)
        data = {'company_name': 'Kanala', 'following_company': [2, 3],
                'following_user': [1, 2], 'following_cause': [1]
                }
        response = client.put('/api/v1/companies/{}/'.format(self.test_slug), data)
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data['company_name'], 'Kanala')

        #test that following company went alright
        self.assertEqual(response.data['following_company'], [2, 3])
        #did the update go to db as well?
        company = Company.objects.get(slug=self.test_slug)
        self.assertEqual([e.pk for e in company.following_company.all()], [2, 3])
        #make sure it's not symmetrical
        company2 = Company.objects.get(pk=2)
        self.assertTrue(len(company2.following_company.all())==0)
        self.assertEqual(company2.comp_followees.all()[0], company)


        #did the following users went allright
        self.assertEqual(response.data['following_user'], [1, 2])
        #did the update go to db as well?
        self.assertEqual([e.pk for e in company.following_user.all()], [1, 2])
        #make sure it is accessible through related name
        user1 = Account.objects.get(pk=1)
        self.assertEqual(len(user1.user_comp_followees.all()), 1)

        #did the following cause went alright?
        self.assertEqual(response.data['following_cause'], [1])
        #did the update go to db as well?
        self.assertEqual(len(company.following_cause.all()), 1)
        cause = Cause.objects.get(pk=1)
        self.assertEqual([e.pk for e in cause.cause_comp_followees.all()], [1])

        #make sure that the following url is also working
        response = client.get('/api/v1/companies/{}/following-companies/'.format(self.test_slug))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        #let's see if path works!
        data = {'following_company': [2]}
        response = client.patch('/api/v1/companies/{}/'.format(self.test_slug), data)
        self.assertEqual(response.status_code, 202)
        company = Company.objects.get(slug=self.test_slug)
        self.assertEqual([e.pk for e in company.following_company.all()], [3])
        company2 = Company.objects.get(pk=2)
        self.assertEqual(len(company2.comp_followees.all()), 0)