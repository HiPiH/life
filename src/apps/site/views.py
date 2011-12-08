from django.utils.translation   import ugettext_lazy as _
from django.http                import HttpResponseRedirect
from django.shortcuts           import render_to_response, get_object_or_404
from django.template            import RequestContext

def index(req):
    out={}
    out['index'] = 1
    return render_to_response('index.html', out, context_instance=RequestContext(req))