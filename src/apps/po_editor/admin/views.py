# coding: utf-8

from django import forms
from django.contrib.admin import widgets as admin_widgets
from django.core.management.commands.compilemessages import compile_messages
from django.core.management.commands.makemessages import make_messages
from django.http import HttpResponseRedirect
from django.template import mark_safe
from django.utils.translation import ugettext as _
from apps.utils.shortcuts import render_to
from pytils import translit
from apps.utils.server_restart import restart
import codecs
import os
import re
import settings

if hasattr(settings, 'DEFAULT_LANGUAGE'):
    DEFAULT_LANGUAGE = settings.DEFAULT_LANGUAGE
else:
    DEFAULT_LANGUAGE = 'ru'

def cur_lang():
    try:
        from apps.langs.models import get_cur_lang
    except:
        get_cur_lang = None
    if get_cur_lang:
        return get_cur_lang()
    return DEFAULT_LANGUAGE 
    

#class LocaleForm(forms.Form):
#    
#    def __init__(self, config, *args, **kwargs):
#        self.config = config
#        self.base_fields={}
#        
#        for prop in config._getPropertyList():
#            self.base_fields[prop.name] = prop.field(label=prop.title, widget=prop.widget,
#                                                     required=prop.required, initial=prop.default)
#            
#        super(ConfigForm, self).__init__(*args, **kwargs)

class PoNode(object):
    def __init__(self, line=None):
        self.content=[]
        if line:
             self.add_line(line)
    
    def add_line(self, line):
        if line.startswith("#, fuzzy"):        #HACK!!!
            return
        self.content.append(line)
        
    def dump(self):
        ret = "%s:\n" % type(self)
#        return ret+("\n".join(self.content))
        return ret+unicode(self.content)+"\n"
    
    def lines(self):
        return self.content

class PoNodeMsg(PoNode):
    name_rep = re.compile(r"[^\w]+")
    
    def __init__(self, line=None):
        super(PoNodeMsg, self).__init__(line)
        self.id=[]
        self.str=[]
        self.set_id=True
        
    def add_id(self, line):
        line=line.strip(" \n")
        line=line.strip("\"")
        self.id.append(line)
        
    def add_str(self, line):
        line=line.strip(" \n")
        line=line.strip("\"")
        self.str.append(line)
        self.set_id = False
    
    def add_line(self, line):
        if self.set_id:
            self.add_id(line)
        else:
            self.add_str(line)
            
    def add_spec_simbols(self, l):
        return map(lambda e: "\"%s\"\n" % e, l)
        
            
    def lines(self):
        ret_id = self.add_spec_simbols(self.id)
        ret_str = self.add_spec_simbols(self.str)
        ret_id[0] = "msgid "+ret_id[0]
        ret_str[0] = "msgstr " + ret_str[0]  
        return ret_id + ret_str

    def dump(self):
        #ret = "%s:\n" % type(self)
        #return ret+(";\n".join(self.id))+"\n---str:\n"+(";\n".join(self.str))
        ret = "%s:\n" % type(self)
        return ret + unicode(self.id)+'\n'+unicode(self.str)+"\n"
    
    def input_name(self):
        name = "_".join(self.id)
        name = translit.translify(name)
        name = self.name_rep.sub("_", name)
        return name
    
    def input_value(self):
        return "\n".join(self.str)
    
    def input_label(self):
        return "\n".join(self.id)
    
    def is_multiline(self):
        return len(self.id)>1
    
    def set_new_value(self, value):
#        print "new value '%s' for %s" % (value, self.id)
        value = value.replace('\r','').replace('\"','\\"')
        value = value.split('\n')
#        print "new '%s', old '%s'" % (value, self.str)
#        if len(value)>1:
#            print value
        self.str = value
        

class PoNodeComment(PoNode):
    pass

class PoReader(object):
    
    def __init__(self, file_name):
        self.file_name = file_name
        self.nodes=[]
        
    def dump(self):
        return "".join(map(lambda e: e.dump(), self.nodes))

    def add_comment(self, line):
        node = None
        if len(self.nodes)>0:
            node = self.nodes[-1]
            if isinstance(node, PoNodeComment):
                node.add_line(line)
            else:
                node = None
        if not node:
            node = PoNodeComment(line)
            self.nodes.append(node)
    
    def read(self):
        f = codecs.open(self.file_name, "r", "utf-8")
        lines = f.readlines()
        f.close()
        
        prev = None
        for line in lines:
            original = line
            if line.startswith("#") or line.startswith("\n"):
                self.add_comment(line)
            elif line.startswith("msgid"):
                l = line[5:]
                node = PoNodeMsg()
                node.add_id(l)
                self.nodes.append(node)
                prev = node
            elif line.startswith("msgstr"):
                l = line[6:]
                assert prev!=None, "Unknown msgid for msgstr ('%s')" % line
                prev.add_str(l)
            else:
                assert prev!=None, "Unknown msgid for msgstr ('%s')" % line
                prev.add_line(line)
                
    def write(self):
        f = codecs.open(self.file_name, "w", "utf-8")
        for node in self.nodes:
            f.writelines(node.lines())
        f.close()        

                
    def get_msg(self, input_name):
        for node in self.nodes:
            if isinstance(node, PoNodeMsg):
                if node.input_name()==input_name:
                    return node
        return None
                
class PoForm(forms.Form):
    
    def __init__(self, po, *args, **kwargs):
        self.po = po
        self.base_fields={}

        prev = None
        for msg in po.nodes:
            if isinstance(msg, PoNodeMsg):
                name = msg.input_name()
                if name!="":
                    if msg.is_multiline():
                        widget = admin_widgets.AdminTextareaWidget
                    else:
                        widget = admin_widgets.AdminTextInputWidget
                    help = mark_safe("\n<br/>".join(prev.lines())) if msg else None 
                    self.base_fields[name] = forms.CharField(
                                                label = msg.input_label(),
                                                widget = widget,
                                                initial = msg.input_value(),
                                                required = False,
                                                help_text = help
                                                )
            prev = msg
            
        super(PoForm, self).__init__(*args, **kwargs)
        
    def save(self):
        for key in self.cleaned_data:
            msg = self.po.get_msg(key)
            assert msg, "Unknown message key '%s'" % key
            msg.set_new_value(self.cleaned_data[key])
        self.po.write()

class LocalePath(object):
    
    @staticmethod
    def get(app):
        return os.path.join(LocalePath.get_app_path(app), 'locale')

    @staticmethod
    def get_app_path(app):
        return os.path.join(settings.PROJECT_SRC_ROOT, app.replace(".", os.path.sep))
    
    def __init__(self, app):
        self.path = self.get(app)
        self.app = app
        self.app_name = app.split(".")[-1]
        
    def makemessages(self):
        saved = os.getcwd()
        os.chdir(LocalePath.get_app_path(self.app))
#        print os.getcwd()
        make_messages(locale = cur_lang(), domain='django', verbosity =0, extensions=['.html', '.eml'])
#    make_messages(locale, domain, verbosity, process_all, extensions)
        os.chdir(saved)
        
    def compilemessages(self):
        saved = os.getcwd()
        os.chdir(LocalePath.get_app_path(self.app))
        compile_messages(locale = cur_lang())
        os.chdir(saved)

    def load(self):
        po_file = os.path.join(LocalePath.get_app_path(self.app), 'locale', cur_lang(), 'LC_MESSAGES', 'django.po')
        
        self.po = PoReader(po_file)
        self.po.read()
        

    
@render_to('po_editor/admin/form.html')
def form(req, app):
    out={}
    assert app in settings.INSTALLED_APPS, "Unknwon app name '%s'" % app
    
    out['locale'] = locale = LocalePath(app)
    locale.makemessages()
    locale.load()
    
    if req.POST:
        out['form'] = form = PoForm(po = locale.po, data=req.POST)
        if form.is_valid():
            form.save()
            locale.compilemessages()
            restart()
    else:
        out['form'] = PoForm(po = locale.po)
    
    return out


@render_to('po_editor/admin/list.html')
def list(req):
    out={}
    
    out['locale_path_list'] = locale_path_list =[]
    

    for app in settings.INSTALLED_APPS:
        locale_path = LocalePath.get(app)
        if os.path.isdir(locale_path):
            locale_path_list.append(LocalePath(app))
    
    return out