# coding:utf-8

from django import template
from django.template import Library, Node
from django.utils.translation   import ugettext_lazy as _

from django.template.loader import render_to_string


register = template.Library()

#@register.simple_tag
#def rubric(address, request):
#    print "!!!!!!!!!!!!!!!!!"
#    return 1


class AjaxNode(Node):
    def __init__(self, title, view_name, opts=None,
                 context_name=None, **kwargs):
        self.title = title
        self.view_name = view_name
        self.deault_template="ajax_view.html"

    def render(self, context):
        
#        try:
#            root = Rubric.objects.filter(system_name = self.system_name)[0]
##            print "Load %s as %s" % (self.system_name, self.var)
#        except Exception, e:
#            root = None
        context['ajax_view_title'] = self.title.strip("\"")
        context['ajax_view_name'] = self.view_name.strip("\"")
        return render_to_string(self.deault_template, None, context)

def ajax_view(parser, token):
    args = token.split_contents()
    tag = args[0]
    
    title = parser.compile_filter(args[1])
    view_name = parser.compile_filter(args[2])    
    return AjaxNode(unicode(title), unicode(view_name))

register.tag(ajax_view)

