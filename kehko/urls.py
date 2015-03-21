from django.conf.urls import patterns, include, url
from django.contrib import admin

from kehko.views import IndexView

urlpatterns = patterns('',
    # Examples:
    url(r'^$', IndexView.as_view(), name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
