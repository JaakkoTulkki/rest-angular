from django.conf.urls import patterns, include, url
from django.contrib import admin

from kehko.views import IndexView
from authentication.views import AccountList

account_urls = patterns('',
    #url(r'^/(?P<username>[0-9a-zA-Z_-]+)$', AccountDetail.as_view(), name='account-detail'),
    url(r'^/$', AccountList.as_view(), name='account-list')
)

urlpatterns = patterns('',
    #url(r'^$', IndexView.as_view(), name='home'),
    url(r'^api/v1/users', include(account_urls)),
    url(r'^api/v1/auth/login/$', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'.*', IndexView.as_view(), name='home'), #I wonder if this is the best way to do it
)
