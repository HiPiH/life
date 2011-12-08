from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.core.management.base import AppCommand, CommandError
from imp import find_module


class Command(AppCommand):
   
    def handle_app(self, app, **options):
        raise NotImplementedError()
   
    def handle(self, *app_labels, **options):
        from django.db import models
        if not app_labels:
            raise CommandError('Enter at least one appname.')
        
        print "Start"        
        for app_name in app_labels:                
            try:
                mod = __import__(app_name, {}, {}, ['correctdb'])
            except (ImproperlyConfigured, ImportError), e:
                raise CommandError("%s. Are you sure your module exists?" % e)
                
            if hasattr(mod, 'correctdb'):
                print "run:%s..." % app_name
                rdb=getattr(mod, 'correctdb')
                rdb.handle()
        
        print "Finish"

