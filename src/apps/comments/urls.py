from django.conf.urls.defaults import *

urlpatterns = patterns('apps.comments.views',
    (r'^$', 'operate'),
    (r'^recall/$', 'operate_recall'),
    )