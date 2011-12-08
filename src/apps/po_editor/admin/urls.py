from django.conf.urls.defaults import *

urlpatterns = patterns('apps.po_editor.admin.views',
    url(r'^$', 'list', name='po_editor_list'),    
    url(r'^form/(?P<app>[\w.]+)/$', 'form', name='po_editor_form'),
)