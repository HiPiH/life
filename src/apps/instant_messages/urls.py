from django.conf.urls.defaults import *

urlpatterns = patterns('apps.instant_messages.views',
    url(r'^window/$', 'window', name="im_window"),
    url(r'^ajax/$', 'ajax', name="im_ajax"),
)