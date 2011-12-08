from django.conf.urls.defaults import *

from apps.captcha import views

urlpatterns = patterns('',
    url(r'^captcha/(?P<captcha_id>\w+)/$', views.captcha_image, name='captcha_image'),
    url(r'^get_new/$', views.get_new_image, name='captcha_get_new'),
)

