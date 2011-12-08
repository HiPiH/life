import re
from django import template
from apps.blog.models import Post
from django.contrib.auth.models import User
from django.contrib.admin import options
from django.utils.safestring import mark_safe
from apps.blog.models import Tag

register = template.Library()

class ChangeListUserFilter(template.Node):
    def __init__(self, obj, user):
        self.obj = obj
        self.user = user

    def render(self, context):
        try:
            cl = template.resolve_variable(self.obj, context)
            user = template.resolve_variable(self.user, context)
        except template.VariableDoesNotExist:
            return ''
        if not user.is_superuser:
            cl.result_list = [li for li in cl.result_list if li.author == user]
        #context[cl] = cl
        return ''

class ChangeDeletedObjects(template.Node):
    def __init__(self, deleted, post):
        self.deleted = deleted
        self.post = post

    def render(self, context):
        try:
            deleted = template.resolve_variable(self.deleted, context)
            post = template.resolve_variable(self.post, context)
        except template.VariableDoesNotExist:
            return ''
        print repr(deleted)
        deleted.extend([mark_safe(repr(li)[1:-1]) for li in post.get_comments()])
        return ''

class TagSize(template.Node):
    def __init__(self, obj, var_name, height):
        self.obj = obj
        self.var_name = var_name
        self.height = height
    
    def render(self, context):
        try:
            weight = float(template.resolve_variable(self.obj, context))
        except template.VariableDoesNotExist:
            return ''
        tag_max = Tag.objects.all().order_by('-weight')
        if tag_max:
            tag_max = tag_max[0].weight
        size = int((weight/float(tag_max))*24)
        context[self.var_name] = size if size> 10 else 10
        context[self.height] = context[self.var_name] + 6
        return ''

class SplitPost(template.Node):
    def __init__(self, obj, teaser, body):
        self.obj = obj
        self.teaser = teaser
        self.body = body
    
    def render(self, context):
        try:
            post_text = template.resolve_variable(self.obj, context)
        except template.VariableDoesNotExist:
            return ''
        tmpl_hr = re.compile(r'\<hr[^\/]*\/\>')
        tmpl_div_start = re.compile(r'\<div')
        tmpl_div_end = re.compile(r'\<\/div')
        tmpl_a_start = re.compile(r'\<a')
        tmpl_a_end = re.compile(r'\<\/a')
        tmpl_em = re.compile(r'\<[\/]?em>')
        hr_match = tmpl_hr.search(post_text)
        if hr_match:
            teaser, body = tmpl_hr.split( post_text, 1 )
            div_starts_count = len( tmpl_div_start.findall( post_text, endpos=hr_match.start() ) )
            div_ends_count = len( tmpl_div_end.findall( post_text, endpos=hr_match.start() ) )
            teaser += '</div>'*(div_starts_count - div_ends_count) + '<div style="clear: both"></div>'
            body = '<div>'*(div_starts_count - div_ends_count) + body
            
            a_starts_count = len( tmpl_a_start.findall( post_text, endpos=hr_match.start() ) )
            a_ends_count = len( tmpl_a_end.findall( post_text, endpos=hr_match.start() ) )
            teaser += '</a>'*(a_starts_count - a_ends_count)
            
            teaser = tmpl_em.sub('', teaser)
            body = tmpl_em.sub('', body)
        else:
            teaser = ''
            body = post_text
        context[self.teaser] = teaser
        context[self.body] = body
        return ''

def do_split_post(parser, token):
    """
        {% split_post <text> on <text teaser> and <text body>%}
    """
    bits = token.contents.split()
    if len(bits) != 6:
        raise template.TemplateSyntaxError("invalid syntax")
    return SplitPost(bits[1], bits[3], bits[5])

def add_deteted_comments(parser, token):
    """
        {% add_deteted_comments <deleted_objects> <Post object>%}
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes exactly two argument" % bits[0])
    return ChangeDeletedObjects(bits[1], bits[2])

def do_change_list_user_filter(parser, token):
    """
        {% change_list_user_filter <ChangeList object> <User object>%}
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes exactly two argument" % bits[0])
    return ChangeListUserFilter(bits[1], bits[2])

def do_get_tag_size(parser, token):
    """
        {% get_tag_size <int weight> as <int size> and <int height>%}
    """
    bits = token.contents.split()
    if len(bits) != 6:
        raise template.TemplateSyntaxError("invalid syntax")
    return TagSize(bits[1], bits[3], bits[5])

register.tag('change_list_user_filter', do_change_list_user_filter)
register.tag('add_deteted_comments', add_deteted_comments)
register.tag('get_tag_size', do_get_tag_size)
register.tag('split_post', do_split_post)