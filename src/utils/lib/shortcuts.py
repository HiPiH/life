from django.shortcuts import get_object_or_404, render_to_response, _get_queryset
from django.http import Http404
from lib.exceptions import Ajax404
from django.template import RequestContext
from lib.http import JsonResponse


def get_object_or_404_ajax(*args, **kwargs):
    try:
        return get_object_or_404(*args, **kwargs)
    except Http404, e:
        raise Ajax404, e

        
def get_pub_object_or_404_ajax(*args, **kwargs):
    try:
        return get_pub_object_or_404(*args, **kwargs)
    except Http404, e:
        raise Ajax404, e


def get_object_or_none(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), an MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None
        
def get_pub_object_or_404(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(is_published=True, *args, **kwargs)
    except queryset.model.DoesNotExist:
        raise Http404('No %s matches the given query.' % queryset.model._meta.object_name)

def get_pub_list_or_404(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    obj_list = list(queryset.filter(is_published=True, *args, **kwargs))
    if not obj_list:
        raise Http404('No %s matches the given query.' % queryset.model._meta.object_name)
    return obj_list
    
def render_to(template):
    """
    Decorator for Django views that sends returned dict to render_to_response function
    with given template and RequestContext as context instance.

    If view doesn't return dict then decorator simply returns output.
    Additionally view can return two-tuple, which must contain dict as first
    element and string with template name as second. This string will
    override template name, given as parameter

    Parameters:

     - template: template name to use
    """
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0], RequestContext(request))
            elif isinstance(output, dict):
                return render_to_response(template, output, RequestContext(request))
            return output
        return wrapper
    return renderer


def ajax_request(func):
    """
    Checks request.method is POST. Return error in JSON in other case.

    If view returned dict, returns JsonResponse with this dict as content.
    """
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            response = func(request, *args, **kwargs)
        else:
            response = {'error': {'type': 405, 
                'message': 'Accepts only POST request'}}
        if isinstance(response, dict):
            resp = JsonResponse(response)
            if 'error' in response:
                resp.status_code = response['error'].get('type', 500)
            return resp
        else:
            return response
    return wrapper
