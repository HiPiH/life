from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from apps.search.finder import search_manager

RESULTS_ON_PAGE = 10

def process_query(request, pagenum=1):
    if request.GET and 'q' in request.GET:
        qry = request.GET['q']
    else:
        qry = ""
    if request.GET and 'ctype' in request.GET:
        ctype = request.GET['ctype']
    else:
        ctype = None
    r = []
    if qry:
        #for li in RMODELS:
            #ct = ContentType.objects.get_for_model(li)
            #r.extend(km.search(qry, ct))
        if ctype:
            ct = ContentType.objects.get(pk=int(ctype))
            m = ct.model_class()
            r = search_manager.search_for_model(qry, m)
        else:
            r = search_manager.search_all(qry)
        pager = Paginator(r, RESULTS_ON_PAGE)
        page = pager.page(pagenum)
        return render_to_response('search/search-results.html', {
            'query': qry,
            'page': page, 
            'paginator': pager},
            context_instance=RequestContext(request))
    else:
        return render_to_response('search/search-results.html', {}, context_instance=RequestContext(request))
