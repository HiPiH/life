from django.conf.urls.defaults import *

urlpatterns = patterns('apps.feedback.views',
    url(r'^form/$', 'form', name="feedback_form"),
)