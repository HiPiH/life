from django.conf.urls.defaults import *
from django.contrib import admin
from urls_base import *

import settings

admin.autodiscover()

urlpatterns += patterns('',
    # Example:
    # (r'^app/', include('app.foo.urls')),

    #(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.PATH_TO_SOMETHING_STATIC}),

    # uncomment this to include fckconnector urls
    #(r'^admin/fckconnector/', include('fckconnector.admin_urls')),

)
