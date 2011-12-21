"""
Kovalenko Pavel (ice.tegliaf@gmail.com)
  
"""
from xml.dom import minidom, Node
import settings
from settings import PROJECT_SRC_ROOT
import os
from django.core.urlresolvers import reverse, resolve2
import re




DEFAULT_MENU = os.path.join(PROJECT_SRC_ROOT, 'apps','site','menu.xml')
root_item=None

def get_attr(node, attr_name):
    for attr in node.attributes.items():
        if attr[0]==attr_name:
            return attr[1]
    raise Exception('Unknown attribute "%s" in "%s"' % (attr_name, node.tagName))


def safe_get_attr(node, attr_name):
    for attr in node.attributes.items():
        if attr[0]==attr_name:
            return attr[1]
    return None


class View(object):
    
    def __init__(self):
        self.pattern = ''
        self.func_name=''
        self.kwargs = {}
        self.ne_kwargs = {}
        
    def _load(self, node):
        try:
            self.pattern = get_attr(node, 'name')        
        except:
            pass
        try:
            self.func_name = get_attr(node, 'function')
        except:
            pass

        for child in node.childNodes:
            if child.nodeType==Node.ELEMENT_NODE:
                #value_ne                
                ne=safe_get_attr(child, 'value_ne')
                if ne:
                    self.ne_kwargs[str(child.tagName)] = get_attr(child, 'value_ne')
                else:
                    self.kwargs[str(child.tagName)] = get_attr(child, 'value')
                
    def exec_func(self,view_name, kwargs):        
        pos = self.func_name.rfind(".")
        app = self.func_name[:pos]
        func_name = self.func_name[pos+1:]
        mod = __import__(app,[],[],[func_name])
        if hasattr(mod, func_name):
            func = getattr(mod, func_name)
            return func(view_name, kwargs)
        raise Exception("Error loading 'function': %s" % self.func_name)
                
    def match(self, view_name, kwargs):
        if self.pattern:
            p = re.match(self.pattern, view_name)
            if p:
                for aname in self.ne_kwargs:
                    if aname in kwargs and self.ne_kwargs[aname]==kwargs[aname]:
                        return False                
                for aname in self.kwargs:
                    if aname in kwargs and self.kwargs[aname]!=kwargs[aname]:
                        return False
                if self.func_name:
                    return self.exec_func(view_name, kwargs) 
                return True
        else:
            if self.func_name:
                return self.exec_func(view_name, kwargs)
        
        return False
        
class Item(object):
    
    
    def __init__(self):
        self.name=''
        self.childs=[]
        self.url_name=''
        self.url_attrs={}
        self.views=[]
        self.selected=False

    __unicode__ = lambda self: self.name
    
    def selected_item(self):
        for item in self:
            if item.selected:
                return item
        return None
    
    def __iter__(self):
        for child in self.childs:
            yield child
            
    def _load(self, node):
        for attr in node.attributes.items():
            setattr(self, attr[0], attr[1])
            
        for child in node.childNodes:
            if child.nodeType==Node.ELEMENT_NODE:
                if child.tagName=='childs':
                    self._load_childs(child)
                
                if child.tagName=='url':
                    self._load_urls(child)
    
                if child.tagName=='view':
                    self._load_view(child)


    def _load_childs(self, childs):
        for child in childs.childNodes:
            if child.nodeType==Node.ELEMENT_NODE and child.tagName=='item':
                item = Item()
                item._load(child)          
                self.childs.append(item)

    def _load_urls(self, url):
        self.url_name = get_attr(url, 'name')
        self.url_attrs={}
        for url_attr in url.childNodes:
            if url_attr.nodeType==Node.ELEMENT_NODE:
                self.url_attrs[str(url_attr.tagName)]=get_attr(url_attr, 'value')

    def _load_view(self, view_node):
        view = View()
        view._load(view_node)        
        self.views.append(view)

                
    def get_absolute_url(self):
        if self.url_name:
            return reverse(self.url_name, kwargs=self.url_attrs)
        else:
            if len(self.childs)>0:
                return self.childs[0].get_absolute_url()
        return "#MenuUrlNotFound"
    
    def select(self, view_name, view_kwargs):
        for child in self:
            if child.select(view_name, view_kwargs):
                self.selected=True
                
        for view in self.views:
            if view.match(view_name, view_kwargs):                
                self.selected=True
                return True
        
        return False
                
    
class Menu(object):
    
    def __init__(self):
        self.root_item = None
    
    def load_from_xml(self):
        f = open(os.path.join(settings.PROJECT_ROOT, DEFAULT_MENU), "r")
        xml_document = "".join(f.readlines())
        
        f.close()
        doc = minidom.parseString(xml_document)
        for child in doc.childNodes:
            if child.nodeType==Node.ELEMENT_NODE and child.tagName=='item':
                self.root_item = Item()
                self.root_item._load(child)
                
    def select(self, url):
        resolve_value =  resolve2(url)
        if not resolve_value:
            return
        
        ret, args, view_kwargs = resolve_value
        
        if not hasattr(ret, '_callback_str'):
            return 

        url_view_name =  ret._callback_str
        if ret._callback_str == 'apps.events.views.one':
            url_view_name = ret.name.replace('events_one_meeting','events_meeting')
        
        for item in self.root_item:
            if item.select(url_view_name, view_kwargs):
                return True
        return False
                
#    def test(self):
#        from django.template.loader import render_to_string
#        return render_to_string('xml_menu/test.html', {'root': self.root_item})

        

