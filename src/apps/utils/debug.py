# coding: utf-8
"""
"          SVN: $Id: debug.py 242 2008-11-20 14:25:52Z ice $
"  Last Update: $Author: ice $
"      Version: $Revision: 242 $
"        Datum: $Date: 2008-11-20 17:25:52 +0300 (Чт, 20 ноя 2008) $
"       E-Mail: Kovalenko Pavel <ice.tegliaf@gmal.com>
"      Comment: Help file    
"""
import settings

import types, sys, codecs, os
from django.utils.encoding import force_unicode

#def prEx(key,val,livel,maxLivel):
#    if len(key)>0 and key[0]=='_': return ''
#    if livel==maxLivel:
#        return "<li>%s: %s</li>" % (key, val.__class__.__name__);
#    
#    if type(val) is types.MethodType:
#        return "<li>%s: %s</li>" % (key, val.__class__.__name__);
#    
#    if type(val) is types.DictType and key!='__dict__':
#        return "<li>%s: %s</li>%s" % (key, val.__class__.__name__, repr(val));
#    
#    if type(val) is types.StringType or type(val)==types.ListType or type(val)==types.TupleType:
#        return "<li>%s: %s</li>%s" % (key, val.__class__.__name__, repr(val));
#    
#    out='<ul>'    
#    for k in dir(val):     
#        out+=prEx(k,getattr(val, k),livel+1,maxLivel)
#    out+='</ul>'
#    return "<li>%s: %s</li>%s" % (key, val.__class__.__name__, out);
#        
#def pr(obj,maxLivel=3):
#    from django.http import HttpResponse
#    return HttpResponse(prEx('',obj,0,maxLivel))



class FollowSQL(object):
    #django.core.context_processors.debug
    def out(self, str):                
        if hasattr(self, 'f'):            
            self.f.write(unicode(str))
            self.f.flush()
        if self.localOut:
            print str,
            sys.stdout.flush()
            

#    def process_request(self, request):
#        ####
#        if settings.DEBUG and not request.META['PATH_INFO'].startswith('/media/'):
#            import time
#            time.sleep(1)
#        ####
#        pass

    def is_resource(self, req):
        return req.META['PATH_INFO'].startswith('/media/')


    def process_response(self, request, response):
        if self.is_resource(request):
            return response

        from django.core.context_processors import debug
        import settings
        self.localOut=hasattr(settings,'CONSOLE_SQL_LOG') and settings.CONSOLE_SQL_LOG
        if settings.DEBUG and request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
            try:
                queries=debug(request)['sql_queries']
            except:
                queries=None
            if queries:
                if not hasattr(self,'f') :
                    try:
                        self.f = codecs.open(os.path.join(settings.PROJECT_ROOT, 'sql.log'), 'wt', 'utf-8')
                    except:
                        pass
#                if len(queries)>0:
                    #self.out('-----------------------------------------------\n')
                i=1
                for query in queries:
                    sql = force_unicode(query['sql'])
#                    sql = sql[:1024]
                    self.out(u'%03d:    %s: %s\n\n' % (i, force_unicode(query['time']), sql))
                    i=i+1               

#                if len(queries)>0 and self.localOut:
#                    print '-----------------------------------------------\n'
        return response

    