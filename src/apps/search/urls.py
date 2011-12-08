# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('apps.search.views',
        (r'^$', 'process_query', ),
        (r'^(?P<pagenum>[0-9]\d*).html$', 'process_query', ),
)

