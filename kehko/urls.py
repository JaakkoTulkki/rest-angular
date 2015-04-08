from django.conf.urls import patterns, include, url
from django.contrib import admin

from kehko.views import IndexView
from actions.views import CompanyActions
from authentication.views import AccountList, AccountDetail, RestrictedView, UserCauses
from causes.views import CauseList, CauseDetail, CauseMemberCreate, CauseMemberUpdate
from companies.views import CompanyFollowingCompanies, CompanyList, CompanyDetail, ProductList, ProductDetail
from images.views import ImageList
from news.views import NewsList
from values.views import ValueList, ValueDetail

account_urls = patterns('',
    url(r'^/(?P<username>[0-9a-zA-Z_-]+)/causes/$', UserCauses.as_view(), name='account-causes'),
    url(r'^/(?P<username>[0-9a-zA-Z_-]+)/$', AccountDetail.as_view(), name='account-detail'),
    url(r'^/$', AccountList.as_view(), name='account-list')
)

cause_urls = patterns('',
    url(r'^/$', CauseList.as_view(), name='campaign-list'),
    url(r'^/(?P<slug>[0-9a-zA-Z_-]+)/$', CauseDetail.as_view(), name='campaign-detail'),
)

cause_member_urls = patterns('',
    url(r'^/(?P<pk>[0-9]+)/$', CauseMemberUpdate.as_view(), name='causemember-update'),
    url(r'^/$', CauseMemberCreate.as_view(), name='causemember-create'),
)

company_urls = patterns('',
    url(r'^/$', CompanyList.as_view(), name='company-list'),
    url(r'^/(?P<slug>[0-9a-zA-Z_-]+)/actions/$', CompanyActions.as_view(),
        name='company-actions'),
    url(r'^/(?P<slug>[0-9a-zA-Z_-]+)/following-companies/$', CompanyFollowingCompanies.as_view(),
        name='company-following-company'),
    url(r'^/(?P<slug>[0-9a-zA-Z_-]+)/$', CompanyDetail.as_view(), name='company-detail'),
)

image_urls = patterns('',
    url(r'^/$', ImageList.as_view(), name='image-list'),
)

news_urls = patterns('',
    url(r'^/$', NewsList.as_view(), name='news-list'),
)

product_urls = patterns('',
    url(r'^/(?P<company>[0-9a-zA-Z_-]+)/$', ProductList.as_view(), name='product-list'),
    url(r'^/(?P<company>[0-9a-zA-Z_-]+)/(?P<product>[0-9a-zA-Z_-]+)/$', ProductDetail.as_view(), name='product-detail')
)

value_urls = patterns('',
    url(r'^/$', ValueList.as_view(), name='value-list'),
    url(r'^/(?P<slug>[0-9a-zA-Z_-]+)/$', ValueDetail.as_view(), name='value-detail'),
)

urlpatterns = patterns('',
    #url(r'^$', IndexView.as_view(), name='home'),
    url(r'^api/v1/causes', include(cause_urls)),
    url(r'^api/v1/cause-members', include(cause_member_urls)),
    url(r'^api/v1/companies', include(company_urls)),
    url(r'^api/v1/images', include(image_urls)),
    url(r'^api/v1/news', include(news_urls)),
    url(r'^api/v1/products', include(product_urls)),
    url(r'^api/v1/users', include(account_urls)),
    url(r'^api/v1/values', include(value_urls)),
    url(r'^api/v1/auth/login/$', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^restricted/$', RestrictedView.as_view()),  #for testing purposes
    url(r'.*', IndexView.as_view(), name='home'), #I wonder if this is the best way to do it
)
