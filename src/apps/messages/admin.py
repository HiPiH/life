from django.contrib.auth.models import User
from django.contrib             import admin
from django.utils.translation   import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django import forms

from models           import UsersCommunication, MessageCommunication 
   
class UsersCommunicationAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'count_mes_a', 'count_mes_a_new', 'count_mes_r', 'count_mes_r_new', )
   
#admin.site.register(UsersCommunication, UsersCommunicationAdmin)
#admin.site.register(MessageCommunication)
