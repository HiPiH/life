from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic import date_based

from models import Post

urlpatterns = patterns('apps.blog.views',
    url ( r'^$', 'index', name = "blog_index" ),
    url(r'^posts/(?P<author>[-\w]+)/(?P<date>\d{4}-\d{2}-\d{2})/(?P<slug>[-\w]+)/$', 'post_detail', name="blog_post_detail"),
    url(r'^posts/(?P<author>[-\w]+)/(?P<date>\d{4}-\d{2}-\d{2})/(?P<slug>[-\w]+)/edit/$', 'edit_post', name="blog_edit_post"),
    url(r'^posts/(?P<author>[-\w]+)/(?P<date>\d{4}-\d{2}-\d{2})/(?P<slug>[-\w]+)/delete/$', 'delete_post', name="blog_delete_post"),
    url(r'^posts/(?P<author>[-\w]+)/((?P<page_num>\d+).html)?$', 'post_list', name='blog_post_list'),
    url(r'^((?P<page_num>\d+).html)?$', 'index'),
#    url(r'^section/(?P<sectID>\d+)/((?P<page_num>\d+).html)?$', views.section, name="section"),
    url(r'^tag/(?P<tagID>\d+)/((?P<page_num>\d+).html)?$', 'tag', name="tag"),
    
    url(r'^posts/(?P<author>[-\w]+)/last/$', 'last_posts'),
    url(r'^posts/(?P<author>[-\w]+)/friendsposts/$', 'friends_last_posts'),
    url(r'^posts/(?P<author>[-\w]+)/createpost/$', 'create_post', name = 'blog_create_post'),
    
    url(r'^authors/((?P<page_num>\d+).html)?$', 'authors', name="blog_authors"),


    url(r'^ajax_user_posts/(?P<id>\d+)/((?P<page_num>\d+).html)?$', 'ajax_user_posts', name="blog_ajax_user_posts"),
    
    # new replies
    url ( r'^posts/new_replies.html$', 'new_replies', name = 'blog_new_replies' ),
    
    )
