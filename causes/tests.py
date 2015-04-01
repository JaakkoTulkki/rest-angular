from rest_framework.test import APIClient, APIRequestFactory, APITestCase, force_authenticate
from rest_framework.reverse import reverse
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import status

from authentication.models import Account
from causes.models import CauseMembers, Cause
from companies.models import Company, Product

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

        #create couple of companies
        self.limited = Company.objects.create(company_name="limited", account_owner=self.cause_man)
        self.corporated = Company.objects.create(company_name="corporated", account_owner=self.cause_man)

        #create some products for companies
        self.limited_product = Product.objects.create(name="soap", description="smells good",
                                                      price=22, owner=self.limited)
        self.limited_product2 = Product.objects.create(name="comb", description="keeps hair in order",
                                                       price=1.5, owner=self.limited)
        self.corporated_product = Product.objects.create(name="car", description="electric car",
                                                         price=100000, owner=self.corporated)
        self.corporated_product2 = Product.objects.create(name="book", description="read stuff",
                                                         price=23, owner=self.corporated)
        self.corporated_product3 = Product.objects.create(name="food", description="delicious stuff",
                                                         price=23, owner=self.corporated)

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

        #create CauseMember
        cause_pk = response.data['id']
        product_pks = sorted([self.corporated_product.pk, self.corporated_product2.pk])
        data = {'cause': cause_pk, 'company': self.corporated.pk, 'products': product_pks}
        response = client.post('/api/v1/cause-members/', data)
        self.assertEqual(response.status_code, 201)
        causemember = CauseMembers.objects.get(cause__pk=cause_pk)
        self.assertEqual(len(causemember.products.all()), 2)
        self.assertEqual(causemember.products.all()[0], self.corporated_product)
        cause = Cause.objects.get(slug=slug)
        self.assertEqual(len(cause.members.all()), 1)
        self.assertEqual(len(cause.members.all()[0].products.all()), 2)

        #update causemember
        causemember_pk = causemember.pk
        product_pk = self.corporated_product3.pk
        data = {'cause': cause_pk, 'products': [product_pk], 'company': self.corporated.pk}
        #first chek that it works
        response = client.get('/api/v1/cause-members/{}/'.format(causemember_pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['products'], product_pks)

        response = client.put('/api/v1/cause-members/{}/'.format(causemember_pk), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['products'], sorted([self.corporated_product.pk, self.corporated_product2.pk,
                                                            self.corporated_product3.pk]))

        #now update Save Water cause
        #First with falsy data
        data = {'description': ""}
        response = client.put('/api/v1/causes/{}/'.format(slug), data)
        self.assertEqual(response.status_code, 400)

        #now update the cause with correct data
        #add sponsors, values, user followers and cause members
        cause = Cause.objects.get(slug=slug)
        company_pks = sorted([self.corporated.pk, self.limited.pk])
        user_pks = sorted([self.cause_man.pk, self.normal_user.pk])

        data = {'name': 'Save Water-Resources', 'description': "Where's the justice",
                'sponsors': company_pks, 'followers': user_pks,
                }
        response = client.put('/api/v1/causes/{}/'.format(slug), data)
        self.assertEqual(response.status_code, 202)

        #check that the new stuff is saved and the slug is the same!!
        response = client.get('/api/v1/causes/{}/'.format(slug))
        self.assertEqual(response.status_code, 200)

        #check for sponsors
        cause = Cause.objects.get(slug=slug)
        self.assertEqual(cause.name, 'Save Water-Resources')
        self.assertEqual([e.pk for e in cause.sponsors.all()], company_pks)
        #make sure the reverse works
        self.assertEqual(len(self.corporated.cause_set.all()),1 )
        self.assertEqual(self.corporated.cause_set.all()[0].slug, slug)

        #check for followers (users)
        self.assertEqual(len(cause.followers.all()), 2)
        self.assertEqual(len(self.cause_man.cause_following.all()), 1)
        self.assertEqual(self.cause_man.cause_following.all()[0], cause)

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