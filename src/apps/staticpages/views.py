from apps.staticpages.models import Page
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
import settings
from lib.shortcuts import render_to


@render_to('staticpages/page.html')
def page(req, address, path_address=''):
    out={}
    
    if settings.DEBUG:
        page, created = Page.objects.get_or_create(address = address, published = True)
        if created:
            page.title = address
            page.save()
    else:
        page = get_object_or_404(Page, address=address, published=True)
        
    out['page'] = page 
    return out
