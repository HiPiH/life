# coding=utf8
from django import template
from django.core.urlresolvers import reverse
from django.utils.translation   import ugettext_lazy as _
import sys

register = template.Library()
  
@register.simple_tag
def trans_app_name(app_name):
    try:
        app = sys.modules['apps.' + app_name.lower()]
        return app.app_label.capitalize()
    except:
        if app_name.lower() == 'auth':
            return _("auth")
        elif app_name.lower() == 'comments':
            return _("comments")
        else:
            return _(app_name)
        
@register.inclusion_tag('menu.html')
def include_menu(menu, menu_id, request):
    return {
        'menu_id': menu_id,
        'menu': menu,
        'request': request,
    }
    
@register.inclusion_tag('paginator.html', takes_context=True)
def paginate(context, view_name):
    base_url = reverse(view_name)
    return {
        'base_url': base_url,
        'page': context['page'],
    }
    
@register.inclusion_tag('comments/comments.html')
def include_comments(obj):
    return {
        'obj': obj,
    }