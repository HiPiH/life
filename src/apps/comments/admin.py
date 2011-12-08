from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from apps.comments.models import CommentNode, Recall

class CommentNodeAdmin(admin.ModelAdmin):
    date_hierarchy= 'pub_date'
    list_display = ('ban_control', 'pub_date', 'author_control', 'ip_control', 'published', 'body', 'commented_obj_link')
    list_display_links = ('pub_date',)
    search_fields = ['body']
    fieldsets = (
        (None, {
            'fields': ('content_type', 'object_id', 'author', 'body', 'published')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not hasattr(obj, 'author'):
            obj.author = request.user
        obj.save()

class RecallAdmin(admin.ModelAdmin):
    date_hierarchy= 'pub_date'
    list_display = ('pub_date', 'author', 'published', 'body', 'commented_obj_link')
    list_display_links = ('pub_date',)
    search_fields = ['body']
    fieldsets = (
        (None, {
            'fields': ('content_type', 'object_id', 'author', 'body', 'published')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not hasattr(obj, 'author'):
            obj.author = request.user
        obj.save()

#admin.site.register(CommentNode, CommentNodeAdmin)
#admin.site.register(Recall, RecallAdmin)