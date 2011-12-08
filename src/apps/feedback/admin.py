# coding: utf-8
from django.utils.translation   import ugettext_lazy as _
from django.contrib             import admin

from models import *

#Город
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('author','fio','phone','email','pub_date')
    search_fields = ('fio','email','text')
    date_hierarchy = 'pub_date'
admin.site.register(Feedback, FeedbackAdmin)