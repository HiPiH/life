# -*- coding: utf-8 -*-
###############################
# Author: Kovalenko Pavel (ice.tegliaf@gmail.com)
# Version: 1 (alpha)
# Revision: $Rev: 4203 $
# Last update: $Date: 2009-04-16 15:43:12 +0400 (Чт, 16 апр 2009) $
# Update author: $Author: ice $
###############################
from django.forms import widgets
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db import models as django_models
import settings
import pickle
import models
import types
import time
import os
#import pickle
#from apps.utils.logger import log

__all__ = ('Int', 'Float', 'Bool', 'String', 'Text', 'Enum', 'Container', 'aggregator', 'ConfigForm', 'Image')

#CONFIG_SAVED_VALUES = False


if hasattr(settings, 'CONFIG_EXPIRE'):
    CONFIG_EXPIRE = settings.CONFIG_EXPIRE
else:
    if settings.DEBUG:
        CONFIG_EXPIRE = 20
    else:
        CONFIG_EXPIRE = 300 # 5 min
        
#log.write("start Config CONFIG_EXPIRE='%s'" %  CONFIG_EXPIRE)
     

PropertyUnknown=0
PropertyInt=1
PropertyFloat=2
PropertyText=3
PropertyBool=4
PropertyString=5
PropertyEnum=5
PropertyImage=6

class Propery(object):
    "Прототип для типизировhelpанных свойств"
    
    type=PropertyUnknown
    widget=widgets.TextInput
    field = forms.CharField
    name=None
    required = False
    
    
    def __init__(self, default, widget=None, title=None, required=False, onChange=None):
        "Инициализация свойства конфига"
        self.default=default
        self.title=title
        self.value=None
        self._model=None
        self.onChange=onChange
        self.widget = widget or self.widget
        self.required=required
        self._exp_time=0
        if isinstance(self.widget, type):
            self.widget = self.widget()
         

    def render(self):
        """
        Возвращает HTML элеменна формы, для ввода данных
        используеться для формирования интерфейса администрирования
        """
        return self.widget.render(name=self.name, value=self.getValue()) 
        
    getTitle = lambda (self): self.title if self.title else self.name
    
    def _load(self, force=False):
        self.container._load(force)
        
        if not self._model or self._exp_time < time.time() or force:
            try:            
                self._model=models.Property.objects.get(name=self.name, container=self.container._model)
#                log.write("loaded: property %s.%s" % (self.container._name, self.name ))
                self.value = self._model.value
            except Exception, e:
                self._model = models.Property(name=self.name, container=self.container._model)
#                log.write("error: '%s.%s': %s" % (self.container._name, self.name, e.message))                
#                log.write("new: property %s.%s" % (self.container._name, self.name))
            
            
#            try:
#                if self._model.value :            
#                    self.value = pickle.loads(str(self._model.value))
#                #log.write("property %s.%s unpacked" % (self.container._name, self.name))
#            except Exception, e:
#                self.value = "error: %s.%s pickle.loads" % (self.container._name, self.name)
#                #log.write("error: %s.%s unpacked" % (self.container._name, self.name))


            self._exp_time = time.time() + CONFIG_EXPIRE
        
        
    def getValue(self):
        """
        Возвращает типипзированное значение свойства.
        Используется кеширование в память, т.е. загрузка данных из БД
        производится только один раз при первом обращении. 
        """
        self._load()
        return self._format(self.value) if self.value!=None else self._format(self.default)
    
    #TODO added value validation
    def setValue(self, value):
        """
        Установить значение для свойства.
        Установка производиться только, если устанавливаем новое значение. 
                 
        """
        #TODO UnicodeWarning: Unicode unequal comparison failed to convert both arguments to Unicode - interpreting them as being unequal
        #print self.getValue(),',', self._format(value)
        self._load(True)
        #print "container %s model = %s" % (self.container._name, self.container._model) 
        #print "property %s.%s model = %s" % (self.container._name, self.name, self._model)
        oldValue = self.getValue()
        newValue = self._format(value)
#        print type(oldValue), type(newValue)
        if oldValue!=newValue :
            if not self.container._model.id:
                self.container._model.save()
                #print "container %s saved" % (self.container._name)
#                log.write("saved: container %s" % (self.container._name))
                self._model.container=self.container._model
            self._model.value = self.value = self._format(value)
#            print type(self.value)
#            self._model.value=u'%s' % pickle.dumps(self.value)
#            print type(self._model.value)
            self._model.save()
            
            if self.onChange and callable(self.onChange):
                self.onChange(self.container, oldValue, newValue)
#            log.write("saved: property %s.%s" % (self.container._name, self.name))
#        else:
#            log.write("no saved: value unique '%s'='%s'" % (oldValue, newValue))
            
            
    def _format(self, value):
        return value
           
        
    __call__ = getValue
#    __unicode__ = getValue

    def validate(self, value):
        return True

        
class Int(Propery):
    "Целочисленные свойства"
    type=PropertyInt
    field=forms.IntegerField

    def __init__(self, *args, **kwargs):
        super(Int, self).__init__(*args, **kwargs)
        self.required=True
    
    def __int__(self):
        return self.getValue()
    
    def _format(self, value):
        return int(value)

class Float(Propery):
    "Свойства вещественного типа"
    type=PropertyFloat
    field=forms.BooleanField
    
    def _format(self, value):
        return float(value)
    
class Bool(Propery):
    "Свойства типа флаг"
    type=PropertyBool
    widget = widgets.CheckboxInput
    
    def _format(self, value):
        return bool(int(value)) if type(value)==types.UnicodeType else bool(value) 
        
class String(Propery):
    "Свойства типа строка"
    type=PropertyString
    widget = widgets.TextInput
    
    def __init__(self, default, max_length=255, **kwargs):
        if type(default)!=types.UnicodeType:
            default = unicode(default)
        
        super(String, self).__init__(default=default, **kwargs)
        self.max_length=max_length
        
#        if type(default)!=types.UnicodeType:
#            raise Exception("Default for property.String mast be unicode type.")

    def _format(self, value):
        return unicode(value)

class Text(Propery):
    "Свойства типа текст"
    type=PropertyText
    widget = widgets.Textarea
    
    def __init__(self, default, max_length=32000, **kwargs):
        if type(default)!=types.UnicodeType:
            default = unicode(default)
        
        super(Text, self).__init__(default=default, **kwargs)
        self.max_length=max_length
        self.widget = widgets.Textarea(attrs={'cols':80})
        
#        if type(default)!=types.UnicodeType:
#            raise Exception("Default for property.Text mast be unicode type.")
        
    def _format(self, value):
        return unicode(value)

        
class Enum(Propery):
    "Свойства типа список"
    type=PropertyEnum
    widget = widgets.Select
    
    def __init__(self, default, choices, **kwargs):
        super(Enum, self).__init__(default=default, **kwargs)
        self.choices=choices
        
    def render(self):        
        return self.widget.render(self.name, self.getValue(), choices=self.choices)
    
    
class ConfigForm(forms.Form):
    
    def __init__(self, config, *args, **kwargs):
        self.config = config
        self.base_fields={}
        
        for prop in config._getPropertyList():
            self.base_fields[prop.name] = prop.field(label=prop.title, widget=prop.widget,
                                                     required=prop.required, initial=prop.default)
            
        super(ConfigForm, self).__init__(*args, **kwargs)
    
class Container():
    "Контейнер свойств. "
    
    _form = ConfigForm

    def __init__(self):
        all=dir(self)
        self._name=unicode(self.__class__)
#        #self._name=self._name[8:len(self._name)-2]
        self._model=None
        self._properties=[]
        for name in  all:
            if not name.startswith('_'):
                prop=getattr(self,name)
                prop.name=name
                prop.container=self
                self._properties.append(prop)
    
    def _getPropertyList(self):
        return self._properties
    
    def _getProperty(self, name):
        for prop in self._properties :
            if prop.name==name :
                return prop
        return None 
    
    def _load(self, force):
        if self._model==None or force:
            try:
                self._model = models.Container.objects.get(name=self._name)
#                print "container %s loaded" % self._name
            except :
                self._model = models.Container(name=self._name)
                try:  #<-- initial syncdb bug fix
                    self._model.save()
                except:
                    pass
#                print "container %s new" % self._name
            
    _getTitle =  lambda(self): self._title if '_title' in dir(self) else self._name
    
    def _getData(self):
        ret = {}
        for prop in self._properties :
            ret[prop.name]=prop.getValue()
        return ret
    
    def _setData(self, data):
        for prop in self._properties :
            value = data[prop.name] if prop.name in data else None
            if prop.type==PropertyBool:
                value = value=='on'
            prop.setValue(value)

    @django_models.permalink
    def _get_absolute_url(self):
        return ("apps.config.admin.views.changeList", [self._name])
    
#        for prop in propList:
#            value = req.POST[prop.name] if prop.name in req.POST else None
#            if prop.type==property.PropertyBool:
#                value = value=='on'
#            
#            prop.setValue(value)
#    
#    def is_valid(self, data):
#        print "container validate"
#        return True
#    
#    def set(self, data):
#        return True



class Image(Propery):
    type = PropertyImage
    field = forms.ImageField
    widget = widgets.FileInput
    
    def __init__(self, upload_to, default, **kwargs):
        super(Image, self).__init__(default=default, **kwargs)
        self.upload_to=upload_to
        self.pathready = False
        self.imgpath = ''
    
    def initPath(self):
        if self.pathready:
            return
        self.imgpath = ''.join([os.path.normpath(settings.MEDIA_ROOT), os.path.normpath(self.upload_to)])
        if not os.path.exists(self.imgpath):
            s = os.path.normpath(settings.MEDIA_ROOT)
            for li in os.path.normpath(self.upload_to).split(os.path.sep):
                s = os.path.join(s, li)
                if not os.path.exists(s):
                    os.mkdir(s)
        return
    
    def setValue(self, value):
        oldValue = self.getValue()
        newValue = self._format(value)
        
        self.value=self._format(value)
        self.initPath()
        f = open(''.join([self.imgpath, os.path.sep, self.value.name]), "wb+")
        f.write(self.value.read())
        f.close()
        self._model.value='%s%s' % (self.upload_to, self.value.name)
        self._model.save()
        
        if self.onChange and callable(self.onChange):
            self.onChange(self.container, oldValue, newValue)
        print "property %s.%s saved" % (self.container._name, self.name)
        
    def getValue(self):
        self.container._load(False)
        try:
            self._model=models.Property.objects.filter(name=self.name, container=self.container._model)[0]
            self.value = ImageFile(open(''.join([os.path.normpath(settings.MEDIA_ROOT), os.path.normpath(self._model.value)]), 'r'))
            self.value.url = self.url
        except Exception, msg:
            self._model = models.Property(name=self.name, container=self.container._model)
            self._exp_time = time.time() + CONFIG_EXPIRE
        return self._format(self.value) if self.value!=None else self._format(self.default)
    
    def _get_url(self):
        return ''.join([settings.MEDIA_URL, self.upload_to, os.path.basename(self.value.name)]).replace('//', '/')
    url = property(_get_url)
    
    __call__ = getValue