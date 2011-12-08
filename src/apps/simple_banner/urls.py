from django.conf.urls.defaults import *

urlpatterns = patterns('apps.simple_banner.views',
    url(r'^(?P<id>\d+)/$', 'redirect', name="simple_banner_redirect"),
)