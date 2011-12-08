# coding: utf-8
from django.utils.translation   import ugettext_lazy as _
from django.contrib             import admin

from models import *
from apps.utils.admin import ImagePreviw

#Город
class BannerAdmin(admin.ModelAdmin):
    list_display = ('image_preview','name','published','url',)
    search_fields = ('name',)
    list_editable = ('published',)
    
    
    image_preview = ImagePreviw()
    
admin.site.register(Banner, BannerAdmin)