# coding=utf8
from django import template
from django.template import Library, Node, Variable,TemplateSyntaxError, VariableDoesNotExist
from django.utils.translation   import ugettext_lazy as _
from django.template.loader import render_to_string
from django.utils.encoding import force_unicode
import settings, os, copy, zlib, re, codecs
from django import forms

register = template.Library()

REGISTER_TYPES = ['css', 'js']


if not hasattr(settings, 'FILE_CACHE_ROOT') or not hasattr(settings, 'FILE_CACHE_URL'):
    FILE_CACHE_ROOT =  os.path.join(settings.MEDIA_ROOT, 'cache')
    FILE_CACHE_URL = settings.MEDIA_URL+'cache/'
else:
    FILE_CACHE_ROOT = settings.FILE_CACHE_ROOT
    FILE_CACHE_URL = settings.FILE_CACHE_URL
    
if not hasattr(settings, 'COMPRESS_STATIC_JS'):
    COMPRESS_STATIC_JS = False
else:
    COMPRESS_STATIC_JS = settings.COMPRESS_STATIC_JS
    
if not hasattr(settings, 'COMPRESS_STATIC_CSS'):
    COMPRESS_STATIC_CSS = False
else:
    COMPRESS_STATIC_CSS = settings.COMPRESS_STATIC_CSS
    
    
if not os.path.isdir(FILE_CACHE_ROOT):
    raise Exception("Directory '%s' not found" % FILE_CACHE_ROOT)


context_key = lambda type: "__%s_add" % type

def if_not_add(context, type, value):
    #check file exists
    if settings.DEBUG:
        path_name = os.path.join(settings.MEDIA_ROOT, value)
        if not os.path.exists(path_name):
            raise Exception("Not found '%s'" % path_name)
    
    if value not in context[context_key(type)]: 
        context[context_key(type)].append(value)


class FileAddNode(Node):
    def __init__(self, args, opts=None, context_name=None, **kwargs):
        self.args = args

    def render(self, context):
        for type in REGISTER_TYPES:
            if context_key(type) not in context: 
                context[context_key(type)]=[]
        
        for arg in self.args:
            var = Variable(arg)
            try:
                value =  var.resolve(context)
            except VariableDoesNotExist:
                raise TemplateSyntaxError('"static_add" tag got an unknkown variable: %r' % var.var)
            
            if isinstance(value, forms.BaseForm):
                for js in value.media._js:
                    if_not_add(context, 'js', js)
                    
                if "" in value.media._css:
                    for css in value.media._css[""]:
                        if_not_add(context, 'css', css)
                continue
            
            if callable(value):
                value=value()
                        
            type = value[value.rfind('.')+1:].lower()
            assert type in REGISTER_TYPES, "Unknown compress_static type '%s'. Args: '%s'" % (type, self.args)
            if_not_add(context, type, value)
        return ""
        
def static_add(parser, token):
    return FileAddNode(token.contents.split()[1:])
register.tag(static_add)

    

#def strip_equals(str_list):
#    #strip first
#    for first_num in range(len(str_list[0])):
#        lst = map(lambda x: x[first_num],str_list)
#        if not all(lst[0] is x for x in lst):
#            break
#
#    for last_num in range(len(str_list[0])):
#        last_num = (last_num+1)*-1
#        lst = map(lambda x: x[last_num],str_list)
#        if not all(lst[0] is x for x in lst):
#            break
#        
#    return map(lambda e: e[first_num:last_num+1], str_list)


class FileCompileNode(Node):
    def __init__(self, args, opts=None, context_name=None, **kwargs):
        self.type = args[1]
        assert self.type in REGISTER_TYPES, "Unknown compress_static type '%s'" % args[1]
        self.context_key = '__%s_add' % self.type
        
    def html(self, url):
        if self.type=='css':
            return "<link rel='stylesheet' type='text/css' href='%s'/>" % url
        
        if self.type=='js':
            return "<script type=\"text/javascript\" src=\"%s\"></script>" % url
        return url

    def render(self, context):
        if not self.context_key in context:
            raise Exception("Compress static: Not found '%s' in context" % self.type)
        
        file_list = context[self.context_key]
        if not file_list:
            return ""
        
        if (not COMPRESS_STATIC_JS and self.type=='js') or (not COMPRESS_STATIC_CSS and self.type=='css') :
            buf=""
            for file in file_list:
                buf+=self.html(settings.MEDIA_URL+file)+"\n"
            return buf
        
        files = map(lambda f: os.path.join(settings.MEDIA_ROOT, f), file_list)
        max_mtime = max(map(lambda file: os.stat(file).st_mtime, files))
        
        #make key
        key = zlib.adler32("_".join(file_list))
        name = "%s_%s.%s" % (key, int(max_mtime), self.type)
        cache_name = os.path.join(FILE_CACHE_ROOT, name)
        cache_url = FILE_CACHE_URL + name
        
        if not os.path.isfile(cache_name):
            pattern = re.compile(r"^%s_(\d+).%s$" % (key, self.type))
            
            #check and delete old cached CSS style
            for f in os.listdir(FILE_CACHE_ROOT):
                if pattern.match(f):
                    os.unlink(os.path.join(FILE_CACHE_ROOT, f))
                    
            #create file
            content=[]
            for file in file_list:
#                print "Parse [%s]..." % file
                #content.append(u'\n/* %s */\n' % file)
                try:
                    f = open(os.path.join(settings.MEDIA_ROOT, file), "r")
                    lines = f.readlines()
                    f.close()
                except Exception, e:
                    raise Exception("Can't find '%s'" % os.path.join(settings.MEDIA_ROOT, file))
                    
                
                lines="".join(lines)
                if self.type=='js':
                    from apps.compress_static.jscompressor import JSCompressor
                    js = JSCompressor(2, False)
                    lines = js.compress(lines)
                    
                if self.type=='css':                    
                    p = re.compile(r"\s+")
                    lines = p.sub(" ", lines)
                content.append(lines)


            f = codecs.open(cache_name, "w", "utf-8")
            f = open(cache_name, "w")
            f.writelines(content)
            f.close()
            
#    <link rel='stylesheet' type='text/css' href='{% static_compile css %}'/>
#    <script type="text/javascript" src="{% static_compile js %}"></script>
        return self.html(cache_url)


def static_compile(parser, token):
    return FileCompileNode(token.split_contents())
register.tag(static_compile)