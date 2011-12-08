import re
from django import template
from django.contrib.contenttypes.models import ContentType
from apps.comments.models import CommentNode, Recall
from apps.comments.forms import CommentForm, RecallForm

register = template.Library()

class RecallsCount(template.Node):
    def __init__(self, recalled_object, var_name):
        self.recalled_object = recalled_object
        self.var_name = var_name
    
    def render(self, context):
        obj = template.resolve_variable(self.recalled_object, context)
        context[self.var_name] = Recall.objects.filter(content_type = ContentType.objects.get_for_model(obj), object_id = obj.id).count()
        return ''

def get_recalls_count(parser, token):
    # usage: {% get_recalls_count for <object being recalled> as <variable name> %}
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
    m = re.search(r'for (\w+) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    return RecallsCount(*m.groups())

class Recalls(template.Node):
    def __init__(self, recalled_object, var_name):
        self.recalled_object = recalled_object
        self.var_name = var_name
    
    def render(self, context):
        obj = template.resolve_variable(self.recalled_object, context)
        context[self.var_name] = Recall.objects.filter(content_type = ContentType.objects.get_for_model(obj), 
                                                            object_id = obj.id).order_by('pub_date')
        return ''

def get_recalls(parser, token):
    # usage: {% get_recalls for <object being recalled> as <variable name> %}
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
    m = re.search(r'for (\w+) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    return Recalls(*m.groups())

class RecallFormNode(template.Node):
    def __init__(self, recalled_object, var_name):
        self.recalled_object = recalled_object
        self.var_name = var_name
    
    def render(self, context):
        obj = template.resolve_variable(self.recalled_object, context)
        context[self.var_name] = RecallForm(initial={'content_type': ContentType.objects.get_for_model(obj).id,
                                                      'object_id': obj.id,
                                                      'next': obj.get_absolute_url()})
        return ''

def get_recall_form(parser, token):
    # usage: {% get_recall_form for <object being recalled> as <variable name> %}
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
    m = re.search(r'for (\w+) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    return RecallFormNode(*m.groups())

register.tag('get_recalls_count', get_recalls_count)
register.tag('get_recalls', get_recalls)
register.tag('get_recall_form', get_recall_form)