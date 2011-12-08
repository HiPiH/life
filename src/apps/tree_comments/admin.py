# coding: utf-8
from django.contrib import admin
from django.db import models
from django.utils.translation   import ugettext_lazy as _

from apps.tree_comments.models import *
#from apps.utils.admin import ImagePreviw, ImagePreviwWidget



class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'submit_date', 'is_removed','ip_address', 'content_type', 'object_pk')
    list_editable = ('is_removed', )
    list_filter = ('is_removed',)
    search_fields = ['text']
    date_hierarchy = 'submit_date'
    fieldsets = [(
                  _('Comment'),
                  {'fields':['text', 'is_removed']})
                  ]
    

    
#    def _media(self):
#        super(PostAdmin) 
    
#    class Media:
#        js = (
#              '/media/fckeditor/fckeditor.js',
#              '/media/fckeditor/_media/textarea_all.js',
#              )

admin.site.register(Comment, CommentsAdmin)