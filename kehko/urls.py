from django.conf.urls import patterns, include, url
from django.contrib import admin

from kehko.views import IndexView
from authentication.views import AccountList

account_urls = patterns('',
    #url(r'^/(?P<username>[0-9a-zA-Z_-]+)$', AccountDetail.as_view(), name='account-detail'),
    url(r'^/$', AccountList.as_view(), name='account-list')
)

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'users', include(account_urls)),
    url(r'^admin/', include(admin.site.urls)),
)
