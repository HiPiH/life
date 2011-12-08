from django.conf.urls.defaults import *

urlpatterns = patterns('apps.config.admin.views',
    (r'^(?P<klass>[\w.]+)/$', 'changeList'),
)
