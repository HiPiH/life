# coding: UTF-8

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
import datetime
import os
from django.conf import settings

ERROR_TARGET_NOT_FOUND = 1
ERROR_SOURCE_NOT_FOUND = 2

class VideoManager(models.Manager):
    
    def related(self, obj):        
        ct = ContentType.objects.get_for_model(obj)
        return self.filter(content_type = ct, object_id = obj.id)

    def related_and_processed(self, obj):
        return self.related(obj).filter(error_code=0, processed=True).order_by('date')        
    
    def queue_for_converting(self):
        return self.filter(processed=False, error_code=0).order_by('date')
    

class Video(models.Model):
    objects = VideoManager()
    
    video = models.FileField(_(u'video'), upload_to='video/')
    flv   = models.FileField(_(u'flv'), max_length=255, upload_to='video/flv/', blank=True, null=True)
    processed = models.BooleanField(_(u'processed'), default=False)
    convert_in_process  = models.BooleanField(_(u'processed'), default=False)
    thumb = models.ImageField(_('thumb'), upload_to='video/flv/thumb/')
    date = models.DateTimeField(_('date'), default=datetime.datetime.now)
    
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    owner = generic.GenericForeignKey('content_type', 'object_id', )
    
    #size in Kb
    source_size = models.PositiveIntegerField(blank=True, default=0)
    #size in Kb
    target_size = models.PositiveIntegerField(blank=True, default=0)
    #secconds
    convert_time = models.PositiveIntegerField(blank=True, default=0)
    
    error_code = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        verbose_name = _(u'video')
        verbose_name_plural = _(u'videos')

    @models.permalink
    def get_absolute_url(self):
        return ('video_player', (), {'id': self.id})
#        
#    def delete(self):
#        #os.unlink(os.path.join(settings.MEDIA_ROOT, self.flv.name))
#        return super(Video, self).delete()
#    
#    def get_object(self):
#        return self.content_type.get_object_for_this_type(pk=self.object_id)

    def save(self):
        super(Video, self).save()
        
    def update_source_size(self):
        try:
            self.source_size = os.path.getsize(os.path.normpath(os.path.join(settings.MEDIA_ROOT, self.video.name)))/1024 #convert to Kb
        except:
            self.error_code = ERROR_TARGET_NOT_FOUND
        self.save()        
#
    def convert_to_flv(self, verbosity):
        if self.error_code!=0:
            return False
            
        dt_start = datetime.datetime.now()
        self.convert_in_process=True
        self.error_code=0
        self.save()       
          
        
        try:
            if self.error_code==0:
                if verbosity==1:
                    print "Start convert (%s)" % self.video.name
                    
                #check dir exists
                dirs=[]
                dirs.append(os.path.join(settings.MEDIA_ROOT, 'video'))
                dirs.append(os.path.join(settings.MEDIA_ROOT, 'video','flv'))
                dirs.append(os.path.join(settings.MEDIA_ROOT, 'video','flv','thumb'))
                dirs.append(os.path.join(settings.MEDIA_ROOT, 'video','flv','thumb','tmp'))
                for dir in dirs:
                    if not os.path.isdir(dir):
                        os.mkdir(dir)
                
                
                source = os.path.normpath(os.path.join(settings.MEDIA_ROOT, self.video.name))
                video_name = os.path.splitext(os.path.split(self.video.name)[1])[0]
                target = "%s.flv" % os.path.normpath(os.path.join(settings.MEDIA_ROOT, 'video','flv', video_name))
                thumb = '%s.jpg' % os.path.normpath(os.path.join(settings.MEDIA_ROOT, 'video','flv','thumb', video_name))
                command = "mencoder '%s' -o '%s' -of lavf -oac mp3lame -lameopts abr:br=56 -srate 22050 -ovc lavc -lavcopts vcodec=flv:vbitrate=500:mbd=2:mv0:trell:v4mv:cbp:last_pred=3" % (source, target,)
                convert_ret_code = os.system(command)
                
                os.chdir(os.path.normpath(os.path.join(settings.MEDIA_ROOT, 'video','flv','thumb','tmp')))
                command = "mplayer -ss 2 -frames 1 -vo jpeg: -nosound %s" % source
                thumb_ret_code = os.system(command)
                
                try:
                    self.target_size = os.path.getsize(target)/1024 #convert to Kb
                except:
                    self.error_code = ERROR_TARGET_NOT_FOUND                
                
                if self.error_code==0:                
                    temp_thumb = os.path.normpath(os.path.join(settings.MEDIA_ROOT, 'video','flv','thumb','tmp', '00000001.jpg'))
                    if os.path.isfile(temp_thumb):
                        os.rename(temp_thumb, thumb)
                    self.flv = os.path.join('video','flv','%s.%s') % (video_name, 'flv')
                    self.thumb = os.path.join('video','flv','thumb','%s.%s') % (video_name, 'jpg')
                    self.processed = True
                    
                    #Delete original
                    self.video=""
                    os.unlink(source)
        except:
            try:
                self.target_size = os.path.getsize(target)/1024 #convert to Kb
            except:
                self.error_code = ERROR_TARGET_NOT_FOUND
            
        finally:
            self.convert_in_process=False
            delta = datetime.datetime.now() - dt_start
            self.convert_time = delta.days*86400 + delta.seconds
#            dt_start = 
            self.save()


            