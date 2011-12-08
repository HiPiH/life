
from apps.simple_banner.models import *

class CPBanners(object):
    
    def __init__(self, req):
        self.req = req
        
    def one(self):
        if not hasattr(self, '_one'):
            try:
                self._one=Banner.objects.filter(published=True).order_by("?")[0]
            except:
                self._one = None
        return self._one
    

    
def cp_banners(req):
    return {'cp_banners': CPBanners(req)}


