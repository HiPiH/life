from django.conf.urls.defaults import *

urlpatterns = patterns('apps.messages.views',
    url(r'^$', 'index', name='messages_index'),
    url(r'^(?P<folder>\d+)/$', 'index', name='messages_index'),
    
    url(r'^(?P<show>[new]+)/$', 'index', name='messages_index_new'),
    url(r'^(?P<folder>\d+)/(?P<show>[new]+)/$', 'index', name='messages_index_new'),
    
    url(r'^(?P<communication_id>\d+)/index.html$', 'list', name='messages_list'),
    url(r'^history_(?P<communication_id>\d+)?/index.html$', 'history', name='messages_history'),
    url(r'^history_(?P<communication_id>\d+)?/(?P<pageNum>\d+).html$', 'history', name='messages_history_pagin'),
    
    url(r'^(?P<to_user_id>\d+)/new.html$', 'new', name='messages_new'),
    
    url(r'^generator/$', 'generator', name='messages_generator'),
    #url(r'^(?P<slug_category>[\w-]+)/index.html$', 'category_one', name='services_category_one'),
    #url(r'^(?P<slug_category>[\w-]+)/(?P<pageNum>\d+).html$', 'category_one', name='services_category_one_paged'),
    #url(r'^(?P<slug_category>[\w-]+)/(?P<slug_service>[\w-]+).html$', 'one', name='services_one'),
    
    # HACKS
#    (r'^up/(?P<newsID>\d+)/?$', 'up'),
#    (r'^down/(?P<newsID>\d+)/?$', 'down'),
#    (r'^published/(?P<newsID>\d+)/?$', 'published'),
#    (r'^specmodule/(?P<newsID>\d+)/?$', 'specmodule'),
)