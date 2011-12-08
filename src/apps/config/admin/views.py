from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from apps.config import property, aggregator
from django import forms

def changeList(req, klass ):
    out={}
    
    
    config=aggregator.getClass(klass)
#    out['properties']= propList = config._getPropertyList()    
    out['classTitle'] = config._getTitle()
    
#    if req.method=='POST':
##        if klass.is_valid(req.POST) :
##            klass.save_valid_data()
#
#        for prop in propList:
#            value = req.POST[prop.name] if prop.name in req.POST else None
#            if prop.type==property.PropertyBool:
#                value = value=='on'
##            try:
##                prop.validate(value)
#            prop.setValue(value)
##            except e:
##                print e
#            

    if req.method=='POST':
        myForm = config._form(config, data=req.POST, files=req.FILES, initial=config._getData())
        if myForm.is_valid():
            config._setData(myForm.cleaned_data)
    else:
        myForm = config._form(config, initial=config._getData())
    
#    myForm.fields['test1'] = forms.CharField(label='cool test 1')
    
    

    out['test']=myForm

    return render_to_response('config/admin/changeList.html', out, context_instance=RequestContext(req))