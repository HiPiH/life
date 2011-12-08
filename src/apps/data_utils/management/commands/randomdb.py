from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.core.management.base import AppCommand, CommandError
from imp import find_module
from datetime import datetime

class Command(AppCommand):
   
#    def handle_app(self, app, **options):
#        raise NotImplementedError()
   
    def handle(self, *app_labels, **options):
        from django.db import models
        if not app_labels:
            raise CommandError('Enter at least one appname.')
        
        begin = datetime.today()
        print "Start - %s" % begin
        for app_name in app_labels:
            call_command('reset', app_name)
            mod = None
            try:
                mod = __import__("apps."+app_name, {}, {}, ['randomdb'])
            except (ImproperlyConfigured, ImportError), e:
                print e
            
            if not mod:
                try:
                    mod = __import__(app_name, {}, {}, ['randomdb'])
                except (ImproperlyConfigured, ImportError), e:
                    raise CommandError("%s. Are you sure your module exists?" % e)
                
            if hasattr(mod, 'randomdb'):
                print "run:%s..." % app_name
                rdb=getattr(mod, 'randomdb')
                rdb.handle()
            else:
                print dir(mod)
                print "Unknwon module randomdb in '%s'" % mod.__file__
#        print "Cool"
        print "\nFinish - %s sec." % (datetime.today() - begin).seconds