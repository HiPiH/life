from django.contrib.auth.models import User
import datetime, random  
from django.contrib.auth.models import User
import os
from apps.data_utils import randomize
from apps.instant_messages.models import Message


def handle():
    
    print "\nCorrect IM DB"
    print "Check user.im_incoming"
    errors=0
    
    for user in User.objects.all():
        count = Message.objects.filter(to = user, is_delivered=False).count()
        if user.im_incoming!=count:
            print "ERROR! (user.im_incoming:%s)..." % user,
            user.im_incoming=count
            user.save()
            errors+=1
            print "correct"
             
    
    print "Total error: %s" % errors