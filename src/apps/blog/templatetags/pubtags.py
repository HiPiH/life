import re
from django import template
from apps.blog.models import Post
from django.contrib.auth.models import User
from django.contrib.admin import options
from django.utils.safestring import mark_safe
from apps.blog.models import Tag
from apps.publications.models import PUB_STATUS

register = template.Library()

class GetStatus(template.Node):
    def __init__(self, stat_ind):
        self.stat_ind = stat_ind
        self.statuses = dict(PUB_STATUS)
    
    def render(self, context):
        try:
            stat_ind = template.resolve_variable(self.stat_ind, context)
            context['operable'] = stat_ind == 'PB' or stat_ind == 'AR'
            context['almanacable'] = stat_ind == 'AR'
            return self.statuses[stat_ind]
        except:
            return ''

def do_get_status(parser, token):
    """
        {% get_status <stat_ind> %}
    """
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError("invalid syntax")
    return GetStatus(bits[1])

register.tag('get_status', do_get_status)
