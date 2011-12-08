# coding: utf-8
"""
/-----------------------------------------------\
|   Programming by: Denis Ivanov (Doberman)     |
|   E-mail:         DenDoberman@gmail.com       |
|                   Doberman_Company@mail.ru    |
\-----------------------------------------------/
"""
from django.contrib.auth             import authenticate, login
from django.utils.translation        import ugettext as _
from django.http                     import HttpResponseRedirect
from django.shortcuts                import render_to_response, get_object_or_404
from django.contrib.auth             import logout
from django.contrib.auth.decorators  import login_required
from django.template                 import RequestContext, Template, loader, Context
from django.contrib.auth.models      import User
from django.core.mail                import send_mail
from django.http                     import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

import settings

# CHANGE POSITIONs
@staff_member_required
def changeposition(req, appname=None, modelname=None, first_id=None, first_position=None, second_id=None, second_position=None):
    out={}
    try:
        search_appname = "apps.%s" % appname
        # SEARCH APP WITH THIS PARAMETERS AND CHANGE POSITION
        for app_name in settings.INSTALLED_APPS:
            if u'%s' % app_name == search_appname:
                print app_name
                mod = __import__(app_name, {}, {}, 'models')
                modKlass=getattr(mod, 'models')
                if hasattr(modKlass, modelname):
                    datas = getattr(modKlass, modelname)
                    # OBJECT 1
                    obj1 = datas.objects.get(pk=first_id)
                    obj1.position = first_position
                    obj1.save()
                    
                    # OBJECT 2
                    obj2 = datas.objects.get(pk=second_id)
                    obj2.position = second_position
                    obj2.save()
                    
                    print "Changed"
                    return HttpResponseRedirect('%s' % req.META['HTTP_REFERER'])
    except:
        pass
    
    out['appname'] = appname
    out['modelname'] = modelname
    out['first_id'] = first_id
    out['second_id'] = second_id
    return render_to_response('admin/interfaces/change_position_error.html', out, context_instance=RequestContext(req))
    
    
@staff_member_required
def delattrs(req, appname=None, modelname=None, pk_id=None, attrs=None,):
    out={}

    try:
        # SPLIT ATTRS
        attrs = attrs.split('-')
    
        search_appname = "apps.%s" % appname
        # SEARCH APP WITH THIS PARAMETERS AND DELETE DATAS
        for app_name in settings.INSTALLED_APPS:
            if u'%s' % app_name == search_appname:
                mod = __import__(app_name, {}, {}, 'models')
                modKlass=getattr(mod, 'models')
                if hasattr(modKlass, modelname):
                    datas = getattr(modKlass, modelname)
                    # OBJECT
                    obj = datas.objects.get(pk=pk_id)

                    for f in obj._meta.fields:
                        #print f.attname
                        if f.attname in attrs:
                            try:
                                setattr(obj , '%s' % f.attname, '')
                            except:
                                pass
                    obj.save()
                    return HttpResponseRedirect('%s' % req.META['HTTP_REFERER'])
    except:
        pass
        
    out['appname'] = appname
    out['modelname'] = modelname
    out['pkid'] = pk_id
    out['attrs'] = attrs
    return render_to_response('admin/interfaces/delattrs_error.html', out, context_instance=RequestContext(req))