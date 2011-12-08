import re
from django import template
from django.contrib.contenttypes.models import ContentType
from apps.comments.models import CommentNode
from apps.comments.forms import CommentForm

register = template.Library()

class CommentsCount(template.Node):
    def __init__(self, commented_object, var_name):
        self.commented_object = commented_object
        self.var_name = var_name
    
    def render(self, context):
        obj = template.resolve_variable(self.commented_object, context)
        context[self.var_name] = CommentNode.objects.filter(content_type = ContentType.objects.get_for_model(obj), object_id = obj.id).count()
        return ''

def get_comments_count(parser, token):
    # usage: {% get_comments_count for <object being commented> as <variable name> %}
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
    m = re.search(r'for (\w+) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    return CommentsCount(*m.groups())

class Comments(template.Node):
    def __init__(self, commented_object, var_name):
        self.commented_object = commented_object
        self.var_name = var_name
    
    def render(self, context):
        obj = template.resolve_variable(self.commented_object, context)
        context[self.var_name] = CommentNode.objects.filter(content_type = ContentType.objects.get_for_model(obj), 
                                                            object_id = obj.id).order_by('path', 'pub_date')
        return ''

def get_comments(parser, token):
    # usage: {% get_comments_count for <object being commented> as <variable name> %}
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
    m = re.search(r'for (\w+) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    return Comments(*m.groups())

class CommentsFormNode(template.Node):
    def __init__(self, commented_object, var_name):
        self.commented_object = commented_object
        self.var_name = var_name
    
    def render(self, context):
        obj = template.resolve_variable(self.commented_object, context)
        context[self.var_name] = CommentForm(initial={'content_type': ContentType.objects.get_for_model(obj).id,
                                                      'object_id': obj.id,
                                                      'next': obj.get_absolute_url()})
        return ''

def get_comments_form(parser, token):
    # usage: {% get_comments_count for <object being commented> as <variable name> %}
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
    m = re.search(r'for (\w+) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    return CommentsFormNode(*m.groups())

register.tag('get_comments_count', get_comments_count)
register.tag('get_comments', get_comments)
register.tag('get_comments_form', get_comments_form)