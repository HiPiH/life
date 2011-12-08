
from lib.shortcuts import JsonResponse, ajax_error

try:
    from apps.dblogger import dblogger
except:
    dblogger = False
    
if dblogger:
    from django.views.debug import ExceptionReporter
    import sys
#
#class DbLoggerMiddleware(object):
#    
#    def process_exception(self, request, exception):
#        exc_info = sys.exc_info()
#        report = ExceptionReporter(request, *exc_info)
#        dblogger.exception(exception, report.get_traceback_html())


__all__ = ('Ajax',)

class Ajax(object):
    
    def __call__(self, req):
        if req.method!="POST": 
            return JsonResponse(ajax_error(405, 'Accepts only POST request'))
        
        try:
            ajax_method=req.POST['ajax_method']
            if not hasattr(self, ajax_method):
                return JsonResponse(ajax_error(405,"Unknown ajax method '%s'" % ajax_method))
            method = getattr(self, ajax_method)
            
            post=dict(req.POST)
            del post['ajax_method']
            kwargs = {}
            for name in post:
                value = post[name]
                if len(value)==1:
                    value=value[0]
                kwargs[str(name)] = value
            return JsonResponse(method(req, **kwargs))
            
        except Exception, e:
            try:
                if dblogger:                
                    exc_info = sys.exc_info()
                    report = ExceptionReporter(req, *exc_info)
                    dblogger.exception(e, report.get_traceback_html())
            except:
                pass            
            return JsonResponse(ajax_error(405,"Server Exception: %s:%s" % (e.__class__, e)))