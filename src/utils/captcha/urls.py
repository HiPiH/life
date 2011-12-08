from django.conf.urls.defaults import *

from utils.captcha import views

urlpatterns = patterns('',
    (r'^captcha/(?P<captcha_id>\w+)/$', views.captcha_image),
    (r'^get_new/$', views.get_new_image),
)

