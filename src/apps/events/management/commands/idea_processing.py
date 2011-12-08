from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from apps.events.models import *

from apps.events.config import config

class Command(BaseCommand):
   
    def handle(self, *app_labels, **options):
        verbosity = int(options['verbosity'])
#        if verbosity==1:
#            print "Idea processing..."
        top=Event.objects.filter(state = STATE_IDEA, idea_rang__gt=0).order_by('-idea_rang')[:config.idea_processing_amount()]
        for event in top:
            event.make_idea_to_organization()
#            if verbosity==1:
#                print "%s:'%s' chnage state to '%s'" % (event.id, event.title, event.get_state_display())
        
