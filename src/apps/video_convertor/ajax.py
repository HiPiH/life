from apps.utils.ajax import Ajax
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from apps.video_convertor.models import Video
from django.db import models
import datetime

STATUS_WAIT = 1
STATUS_PROCESS = 2
STATUS_ERROR = 3
STATUS_FINISH = 10

class UploaderAjax(Ajax):

    def progress(self, req, progress_id):
        if progress_id:
            cache_key = "%s_%s" % (req.META['REMOTE_ADDR'], progress_id)
            data = cache.get(cache_key)
            return data
            
#        return -1
        raise Exception("Unknown progress_id")

    def convert_status(self, req, video_id):
        status = STATUS_WAIT
        video = get_object_or_404(Video, pk=video_id)
        #calculate Queue
        queue_sizes=Video.objects.queue_for_converting().aggregate(summ_source_size = models.Sum('source_size'))        
        source_size=Video.objects.filter(processed=True).aggregate(
                                        summ_source_size = models.Sum('source_size'),
                                        summ_convert_time=models.Sum('convert_time')
                                        )
        
        avg_speed=float(source_size['summ_source_size'])/source_size['summ_convert_time'] #kb per secconds
        total_time = float(queue_sizes['summ_source_size'] if queue_sizes['summ_source_size'] else 0)/avg_speed + 60 #(wait for start convertor)
        delta = (datetime.datetime.now() - video.date)
        cur_time = delta.days*86400 + delta.seconds

        if cur_time>total_time:
            if video.convert_in_process:
                cur_time=total_time-1
            else:            
                cur_time=total_time
        progress = float(cur_time * 100) / total_time
        
        if video.convert_in_process:
            status =  STATUS_PROCESS
        elif video.error_code!=0:
            status =  STATUS_ERROR
        elif video.error_code==0 and video.processed:
            status = STATUS_FINISH
            
        return {'progress': progress, 'status': status, 'convert_error':video.error_code}
         



## A view to report back on upload progress:
#
#from django.core.cache import cache
#from django.http import HttpResponse, HttpResponseServerError 
#
#def upload_progress(request):
#    """
#    Return JSON object with information about the progress of an upload.
#    """
#    progress_id = ''
#    if 'X-Progress-ID' in request.GET:
#        progress_id = request.GET['X-Progress-ID']
#    elif 'X-Progress-ID' in request.META:
#        progress_id = request.META['X-Progress-ID']
#    if progress_id:
#        from django.utils import simplejson
#        cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
#        data = cache.get(cache_key)
#        return HttpResponse(simplejson.dumps(data))
#    else:
#        return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')
    