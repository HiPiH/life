
from django.core.files.uploadedfile import UploadedFile
from pytils.translit import translify

old_init = UploadedFile.__init__

def init(self, *args, **kwargs):
    old_init(self, *args, **kwargs)
    self.name = translify(self.name)
    
UploadedFile.__init__ = init