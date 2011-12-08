from django.conf.urls.defaults import *


urlpatterns = patterns('apps.tree_comments.views',
    url(r'^(?P<content_type_id>\d+)/(?P<object_pk>\d+)/post/$', 'post', name="comments_post"),
    url(r'^ajax/$', 'ajax', name="comments_ajax"),
)
