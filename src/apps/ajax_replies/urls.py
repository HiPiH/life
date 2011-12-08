# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns ( 'apps.ajax_replies.views',
    url ( r'^(?P<type>\w+)/(?P<object_id>\d+)/get_replies.html$', 'get_replies', name = 'ajax_replies_get' ),
    url ( r'^(?P<type>\w+)/(?P<object_id>\d+)/add_reply.html$', 'add_reply', name = 'ajax_replies_add' ),
)