
from django.contrib import admin

class GenericAdmin(admin.ModelAdmin):
    class Media:
        js = (
              '/media/tinyfck/tiny_mce.js',
              '/media/textareas.js',
              )
    @staticmethod
    def register(model):
        admin.site.register(model, GenericAdmin)
        
from django_evolution.models import Version, Evolution
admin.site.unregister(Version)
admin.site.unregister(Evolution)
#
from django.contrib.sites.models import Site
admin.site.unregister(Site)