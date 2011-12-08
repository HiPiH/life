from django.conf.urls.defaults import *

urlpatterns = patterns('apps.staticpages.views',
    url(r'^(?P<address>[\w-]+).html$', 'page', name="staticpages_page"),
    url(r'^(?P<path_address>([\w-]+/)*)(?P<address>[\w-]+).html$', 'page'),
)
