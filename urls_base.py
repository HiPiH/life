from django.conf.urls.defaults import *
from django.contrib import admin
import settings
from apps import config
from apps.utils.admin_views import changeposition, delattrs

from apps.search import finder
finder.autodiscover()
admin.autodiscover()
config.autodiscover()
from django.views.generic.simple import redirect_to,direct_to_template
from apps.events.views import index
from django.http import HttpResponseNotFound,HttpResponse
from django.contrib.sitemaps import FlatPageSitemap


def not_found(request):
    return  HttpResponseNotFound(direct_to_template(request,"404.html"))

urlpatterns = patterns('',
    # INDEX PAGE
    (r'^$', 'apps.events.views.index'),
    
    (r'^', include('apps.events.urls')),
    (r'^feedback/', include('apps.feedback.urls')),
    (r'^captcha/', include('apps.captcha.urls')),
    (r'^pages/', include('apps.staticpages.urls')),
    (r'^accounts/', include('apps.accounts.urls')),
    (r'^blog/', include('apps.blog.urls')),
    (r'^replies/', include('apps.ajax_replies.urls')),
    (r'^messages/', include('apps.messages.urls')),
    (r'^tree_comments/', include('apps.tree_comments.urls')),
    (r'^im/', include('apps.instant_messages.urls')),
    (r'^video/', include('apps.video_convertor.urls')),
    
    (r'^filebrowser/', include('filebrowser.urls')),
    
    # FOR ADMIN 
    (r'^admin/config/', include('apps.config.admin.urls')),
    (r'^admin/po_editor/', include('apps.po_editor.admin.urls')),
    #(r'^admin/po_editor/', include('apps.po_editor.admin.urls')),

    (r'^admin/(.*)', admin.site.root),
    
    # Uncomment the next line to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    (r'^admin-media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ADMIN_MEDIA_ROOT }),

    # SPECIAL ADMIN FUNCTIONS
    (r'^changeposition/(?P<appname>[\w-]+)/(?P<modelname>[\w-]+)/(?P<first_id>\d*)/(?P<first_position>\d*)/(?P<second_id>\d*)/(?P<second_position>\d*)/?$', changeposition),
    (r'^delattrs/(?P<appname>[\w-]+)/(?P<modelname>[\w-]+)/(?P<pk_id>\d*)/(?P<attrs>[\w-]+)/?$', delattrs),

    # sitemap.xml
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'flatpages': FlatPageSitemap}}),
    (r'^robots\.txt$',direct_to_template, {'template': 'robots.txt','mimetype':'text/plain'}),
    (r'^files/',include("filebrowser.urls")),
    (r'^rss/',include("apps.rss.urls")),
)
if not settings.DEBUG:
    urlpatterns += patterns('',   (r'^.*$',not_found))

