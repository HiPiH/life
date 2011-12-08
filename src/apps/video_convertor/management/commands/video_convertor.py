from django.conf import settings
from django.core.management.base import BaseCommand
import os
from apps.video_convertor.models import Video
import time
from optparse import make_option
from django.utils.daemonize import become_daemon

TIMEOUT = 60

class Command(BaseCommand):
    
    option_list = BaseCommand.option_list + (
        make_option('--daemonize', action='store', dest='daemonize', default='False',
            type='choice', choices=['True', 'False',],
            help='Daemonize this process or not.\nDAEMONIZE=[True|False]'),
    )        
   
    def handle(self, *app_labels, **options):
        self.verbosity = int(options['verbosity'])
        
        jobfile = os.path.normpath(os.path.join(settings.PROJECT_ROOT, '!job'))
        if not os.path.isfile(jobfile):
            f = open(jobfile, 'w+')
        else:
            if self.verbosity>=1:
                print "Video convertor already runing"
            return
        
        is_daemonize=options.get('daemonize', "False")=="True"
        if is_daemonize:
            if self.verbosity>=1:
                print "Daemonize this process"
            become_daemon()
        else:
            if self.verbosity>=1:
                print "\nStart video_converto in console mode, use --daemonize=True for Daemonize this process =)"
                print "Timeout per step is '%s' sec." % TIMEOUT               
                print "Press Ctrl+C for exit\n\n"            
        
        try:
            self.go()
        finally:
            os.unlink(jobfile)
            
    def go(self):
        while self.step():
            time.sleep(TIMEOUT)        
            
            
    def step(self):
        """ Convert all needed video """
        try:
            unconverted = Video.objects.queue_for_converting()
            while unconverted:
                for video in unconverted:
                    video.convert_to_flv(self.verbosity)
                unconverted = Video.objects.queue_for_converting()
        except KeyboardInterrupt:
            return 0 #exit from main loop
        return 1            
            
        
