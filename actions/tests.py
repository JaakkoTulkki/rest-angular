from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from rest_framework_jwt.views import obtain_jwt_token

from authentication.models import Account
from causes.models import Cause, CauseMembers
from companies.models import Company

class TestActions(APITestCase):
    def setUp(self):
        factory = APIRequestFactory()

        #set up normal user and token
        self.user = Account.objects.create_user(email="action@kehko.com", username="action", password="pwd")
        request = factory.post('/api/v1/auth/login/', {'email': 'action@kehko.com', 'password': 'pwd'})
        response = obtain_jwt_token(request)
        self.token = response.data['token']

        #set up normal user and token
        self.user2 = Account.objects.create_user(email="action2@kehko.com", username="action2", password="pwd")
        request = factory.post('/api/v1/auth/login/', {'email': 'action2@kehko.com', 'password': 'pwd'})
        response = obtain_jwt_token(request)
        self.token2 = response.data['token']

        #set up a company
        self.company = Company.objects.create(company_name="Action", account_owner=self.user)
        #set up a Cause
        self.cause = Cause.objects.create(creator=self.user, name='Action cause', description="action desc")
        #set up a CauseMember
        self.cause_member = CauseMembers.objects.create(company=self.company, cause=self.cause)

        #set up another company
        self.company2 = Company.objects.create(company_name="Action2", account_owner=self.user2)

    def test_action_creation(self):
        client = APIClient()
        data = {'cause': self.cause.pk, 'url': 'http://www.kehko.com'}
        #try to create an action as unauthenticated user
        response = client.post('/api/v1/companies/{}/actions/'.format(self.company.slug), data)
        self.assertEqual(response.status_code, 401)

        #try to create an action as wrong user
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token2)
        response = client.post('/api/v1/companies/{}/actions/'.format(self.company.slug), data)
        self.assertEqual(response.status_code, 403)

        #now login as the correct one
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        response = client.post('/api/v1/companies/{}/actions/'.format(self.company.slug), data)
        self.assertEqual(response.status_code, 201)

        #create another one
        data = {'cause': self.cause.pk, 'url': 'http://www.google.com'}
        response = client.post('/api/v1/companies/{}/actions/'.format(self.company.slug), data)
        self.assertEqual(response.status_code, 201)

        #now login as the user2, for this user's company we have not yet created a CauseMembership
        #but the view should take care of this as well
        #we want to be part of the cause that we created in the setUp method
        data = {'cause': self.cause.pk, 'url': 'http://www.company2.com'}
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token2)
        response = client.post('/api/v1/companies/{}/actions/'.format(self.company2.slug), data)
        self.assertEqual(response.status_code, 201)
        #now make sure that company2 really is a CauseMember
        cause_member = CauseMembers.objects.get(cause__pk=self.cause.pk, company__slug=self.company2.slug)
        self.assertEqual(cause_member.company.company_name, self.company2.company_name)

        #list the actions of the company one
        client.credentials()
        response = client.get('/api/v1/companies/{}/actions/'.format(self.company.slug))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['url'], 'http://www.kehko.com')
        self.assertEqual(response.data[0]['cause_member'], self.cause_member.pk)