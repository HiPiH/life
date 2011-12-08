# coding: utf-8
from django.utils.translation   import ugettext_lazy as _
from django.contrib             import admin

from models import *




#Log
class LogAdmin(admin.ModelAdmin):
    list_display = ('date', 'type', 'subject',)
    list_display_links = ('date', 'type', 'subject',)
    list_filter = ('type', )
    date_hierarchy = "date"

    class Media:
        js = (
              '/media/fckeditor/fckeditor.js',
              '/media/fckeditor/_media/textarea_all.js',
              )
admin.site.register(Log, LogAdmin)
