
from django.utils.translation       import ugettext_lazy as _
from django.contrib import admin
from django.template.loader import render_to_string
from django.forms import widgets

__all__ = ('GenericAdmin', 'ImagePreviw', 'ImagePreviwWidget')

class ImagePreviw(object):
    
    allow_tags = True
    label = short_description = _('Image')

    
    def __init__(self, fields_name='image'):
        self.fields_name=fields_name
    
    def __call__(self, obj):
        assert hasattr(obj, self.fields_name), "Admin Image preview: Unknown field '%s' in '%s'" % (self.fields_name, type(self))
        return render_to_string("admin/utils/image_preview.html", {'image': getattr(obj, self.fields_name), 'obj':obj})
    
class ImagePreviwWidget(widgets.FileInput):
    
    def render(self, name, value, attrs=None):
        input = super(ImagePreviwWidget, self).render( name, value, attrs)
        return render_to_string("admin/utils/image_preview.html", {'image': value,'input':input})
        
        

class GenericAdmin(admin.ModelAdmin):
    class Media:
        js = (
              '/media/fckeditor/fckeditor.js',
              '/media/fckeditor/_media/textarea_all.js',
              )
    @staticmethod
    def register(model):
        admin.site.register(model, type(self))
        
from django_evolution.models import Version, Evolution
try:
    admin.site.unregister(Version)
except:
    pass
try:
    admin.site.unregister(Evolution)
except:
    pass
#

#try:
#    from django.contrib.sites.models import Site
#    admin.site.unregister(Site)
#except:
#    pass
