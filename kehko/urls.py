from django.conf.urls import patterns, include, url
from django.contrib import admin

from kehko.views import IndexView
from authentication.views import AccountList, AccountDetail
from campaigns.views import CampaignList
from companies.views import CompanyList, ProductList
from values.views import ValueList

account_urls = patterns('',
    url(r'^/(?P<username>[0-9a-zA-Z_-]+)/$', AccountDetail.as_view(), name='account-detail'),
    url(r'^/$', AccountList.as_view(), name='account-list')
)

campaign_urls = patterns('',
    url(r'^/$', CampaignList.as_view(), name='campaign-list'),
)

company_urls = patterns('',
    url(r'^/$', CompanyList.as_view(), name='company-list'),
    url(r'/products/$', ProductList.as_view(), name='product-list')
)

value_urls = patterns('',
    url(r'^/$', ValueList.as_view(), name='value-list'),
)


urlpatterns = patterns('',
    #url(r'^$', IndexView.as_view(), name='home'),
    url(r'^api/v1/campaigns', include(campaign_urls)),
    url(r'^api/v1/companies', include(company_urls)),
    url(r'^api/v1/users', include(account_urls)),
    url(r'^api/v1/values', include(value_urls)),
    url(r'^api/v1/auth/login/$', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'.*', IndexView.as_view(), name='home'), #I wonder if this is the best way to do it
)
