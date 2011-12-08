# -*- coding: utf-8 -*-
from django.contrib import admin
from apps.staticpages.models import *
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse

class PageAdmin(admin.ModelAdmin):
    model = Page
    list_display = ('title', 'my_tag_published', 'address_link', 'my_tag_delete', )
    list_filter  = ('published',)
    prepopulated_fields = {'address': ('title',)}
    fieldsets = [
        (None, {
            'fields': ['title', 'address', 'content', 'published', ]
        }),
        (_('SEO options'), {
            
            'fields': ['seo_title', 'seo_keywords', 'seo_description']
        }),
    ]
    
    class Media:
        js = (
              '/media/fckeditor/fckeditor.js',
              '/media/fckeditor/_media/textarea_all.js',
              '/media/js/admin/change_list_controls.js',
              )
              
    def changelist_view(self, request, extra_context=None):
        
        if request.POST and 'action' in request.POST:
            if request.POST['action']=='checkbox_invert':
                model = self.model
                obj = model.objects.get(pk=request.POST['id'])
                value = getattr(obj, request.POST['field'])
                newValue = not value
                setattr(obj, request.POST['field'], newValue)
                obj.save()
                return HttpResponse(u'%d' % newValue)
            
            print request.POST.items()
        
        if not extra_context: extra_context={}
        extra_context.update({
                              'media':mark_safe(self.media),
                              })
        
        return super(PageAdmin, self).changelist_view(request, extra_context)
    
admin.site.register(Page, PageAdmin)