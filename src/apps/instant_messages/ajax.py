from apps.utils.ajax import Ajax
from django.contrib.auth.models import User
from apps.instant_messages.models import Message
from django.db import models
from apps.utils.shortcuts import ajax_error
import datetime
from django.utils.dateformat import time_format
from apps.utils.templatetags.utils import _human_datetime




LAST_MESSAGES_LIMIT = 20
NEW_MESSAGES_LIMIT = 100

class IMAjax(Ajax):
    
    def _msg_format(self, msg, req):
        return {
                                  'date': time_format(msg.create,"H:i"),
                                  'user_name':unicode(msg.author),
                                  #'date': unicode(_human_datetime(msg.create)),
                                  'i': int(msg.author==req.user),
                                  'name': msg.author.get_full_name(),
                                  'text': msg.text
                                  }
    
    def get_settings(self, req):
        if not req.user.is_authenticated():
            return ajax_error(404, 'User not authenticated')
        
        return {
                'full_name': req.user.get_full_name()
                }
    
    def open_user(self, req, user_name):
        if not req.user.is_authenticated():
            return ajax_error(404, 'User not authenticated')
        
        try:
            user_to = User.objects.get(is_active=True, username = user_name)
        except:
            return False
        last_messages=[]
        ids=[]
        for msg in Message.objects.distinct().filter(
                                          models.Q(author = user_to, to = req.user) |
                                          models.Q(author = req.user, to = user_to)
                                          ).order_by('-create')[:LAST_MESSAGES_LIMIT]:
            last_messages.append(self._msg_format(msg, req))
            if not msg.is_delivered and msg.to==req.user:
                ids.append(msg.id)

        Message.objects.filter(id__in=ids).update(is_delivered=True)
        req.user.im_incoming-=len(ids) #TODO: optimize.... to 
        req.user.save()
            
        last_messages.reverse()

        return {
                'user_full_name': user_to.get_full_name(),
                'last_messages': last_messages
                }
        
    def send_msg(self, req, to_user, text):
        if not req.user.is_authenticated():
            return ajax_error(404, 'User not authenticated')
        
        to = User.objects.get(is_active=True, username = to_user)

        msg=Message(
                author = req.user,
                to = to,
                create = datetime.datetime.today(),
                text = text,
                is_delivered = False
                )
        msg.save()
        return self._msg_format(msg, req)
    
    def check_new(self, req):
        if not req.user.is_authenticated():
            return ajax_error(404, 'User not authenticated')
                
        new_list = []
        ids=[]
        for msg in Message.objects.filter(to = req.user, is_delivered=False).order_by('create')[:NEW_MESSAGES_LIMIT]:
            ids.append(msg.id)
            new_list.append(self._msg_format(msg, req))
            
        Message.objects.filter(id__in=ids).update(is_delivered=True)
        req.user.im_incoming-=len(new_list) #TODO: optimize.... to 
        req.user.save()
        return new_list
            
            