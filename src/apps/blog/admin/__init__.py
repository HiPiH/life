# clear
from django.contrib import admin
from django.conf import settings
from django.contrib.contenttypes import generic
from django import forms

from apps.blog.models import Post, Tag
from apps.comments.models import CommentNode
from django.contrib.auth.models import User

class CommentNodeInline(generic.GenericTabularInline):
    model = CommentNode
    extra = 1

class PostAdmin(admin.ModelAdmin):
    date_hierarchy= 'date'
    list_display = ('date', 'author', 'published')
    list_filter = ('published', )
    inlines = [CommentNodeInline]
    fieldsets = (
        (None, {
            'fields': ('author', 'text',
                'published', 'enable_comments', 'tags')
        }),
    )
    filter_horizontal = ('tags',)
    
    def save_model(self, request, obj, form, change):
        if change:
            if (obj.author == request.user) or (User.objects.get(username = request.user.username).is_superuser):
                obj.save()
        else:
            if not hasattr(obj, 'author'):
                obj.author = request.user
            obj.save()
    
    class Media:
        js = (
              '/media/fckeditor/fckeditor.js',
              '/media/fckeditor/_media/textarea_all.js',
              )

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight')
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
    )

admin.site.register(Post, PostAdmin)
#admin.site.register(Section)
#admin.site.register(Tag, TagAdmin)