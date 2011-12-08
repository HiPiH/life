from django.conf.urls.defaults import *

urlpatterns = patterns('apps.video_convertor.views',
    url("^(?P<id>\d+)/$", "player", name="video_player"),
    url("^ajax/$", "ajax", name="video_ajax"),
    url("^upload_(?P<ct_id>\d+)_(?P<id>\d+)/$", "upload", name="video_upload"),
    url("^(?P<id>\d+)/wait/$", "wait_convert", name="video_wait_convert"),
    
)