# coding: utf-8
from django.utils.translation   import ugettext_lazy as _
from django.contrib             import admin

from models import *
from apps.utils.admin import ImagePreviw



#Фото
class PhotoAdmin(admin.TabularInline):
    model = Photo
    fields = ('photo', 'title', 'published', 'author', )

##Видео
#class VideoAdmin(admin.TabularInline):
#    model = Video
#    fields = ('title', 'event', 'created', 'published', )


#Город
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
admin.site.register(City, CityAdmin)

#Район
class MetroAdmin(admin.ModelAdmin):
    list_display = ('name', 'city',)
    list_display_links = ('name', 'city',)
    list_filter = ('city', )
    search_fields = ('name',)
admin.site.register(Metro, MetroAdmin)

#Группа категорий
class CategoryGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
admin.site.register(CategoryGroup, CategoryGroupAdmin)

#Категория
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'group',)
    list_display_links = ('name', 'group',)
    list_filter = ('group', )
    search_fields = ('name',)
admin.site.register(Category, CategoryAdmin)

#Событие
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'img_preview', 'is_idea','is_interzet', 'category','cached_ball', 'date_create', 'author')
    list_editable = ('is_interzet',)
    list_display_links = ('id', 'title',)
    inlines = (PhotoAdmin,  )
    list_filter = ('is_idea','is_interzet')
    search_fields = ('id', 'title', 'description', 'date_create', 'author__username')
    
    img_preview = ImagePreviw('photo')


#    class Media:
#        js = (
#              '/media/fckeditor/fckeditor.js',
#              '/media/fckeditor/_media/textarea_all.js',
#              )
admin.site.register(Event, EventAdmin)

#Встреча
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('event', 'address','place','begin','end','metro','cached_ball', 'author')
    list_display_links = ('event', 'address',)
    list_filter = ('metro', )
    search_fields = ('address','place', 'author__username')
    date_hierarchy = "begin"
admin.site.register(Meeting, MeetingAdmin)


#Черные метки
class BanAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'when', 'who',)
    list_display_links = ('user', 'event', 'who', 'when',)
    date_hierarchy = "when"

    class Media:
        js = (
              '/media/fckeditor/fckeditor.js',
              '/media/fckeditor/_media/textarea_all.js',
              )
admin.site.register(Ban, BanAdmin)

##Комментарий
#class CommentAdmin(admin.ModelAdmin):
#    list_display = ('event', 'user', 'created', 'text',)
#    list_display_links = ('event', 'user', 'text', 'created',)
#    search_fields = ('text',)
#    date_hierarchy = "created"
#
#    class Media:
#        js = (
#              '/media/fckeditor/fckeditor.js',
#              '/media/fckeditor/_media/textarea_all.js',
#              )
#admin.site.register(Comment, CommentAdmin)
