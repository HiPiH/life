from apps.utils.shortcuts import render_to
from django.shortcuts import get_object_or_404
from apps.video_convertor.models import Video
from apps.video_convertor.ajax import UploaderAjax
from apps.video_convertor.forms import VideoForm
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from apps.video_convertor.file_upload import UploadProgressCachedHandler
from django.core.urlresolvers import reverse




ajax = UploaderAjax()


@render_to("video_convertor/player.html")
def player(req, id):
    out={}
    out['video'] = get_object_or_404(Video, pk = id)
    return out

@render_to("video_convertor/upload.html")
def upload(req, ct_id, id):
    out={'ct_id':ct_id, 'id':id}
    
    ct = get_object_or_404(ContentType, pk = ct_id)
    out['object'] = ct.get_object_for_this_type(pk=id)
    
    if req.POST:
#        #add uploader handler for Ajax process
#        req.upload_handlers.insert(0, UploadProgressCachedHandler(req))

        out['form'] = form = VideoForm(req.POST, req.FILES)
        if form.is_valid():
            form.instance.content_type = ct
            form.instance.object_id = id
            form.save()
            form.instance.update_source_size()
            #return HttpResponseRedirect(form.instance.owner.get_absolute_url())
            return HttpResponseRedirect(reverse("video_wait_convert", kwargs={'id':form.instance.id}))
    else:
        out['form'] = VideoForm()
    return out

@render_to("video_convertor/wait_convert.html")
def wait_convert(req, id):
    out={}
    out['video'] = video = get_object_or_404(Video, pk = id)

    
    return out