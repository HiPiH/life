# coding: utf-8
from django import template
from django.utils.translation import ugettext

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from apps.tree_comments.models import Comment

import string
import sys

register = template.Library()

def get_post_url(object):
    content_type_id = ContentType.objects.get_for_model(type(object))
    return reverse('comments_post', kwargs={
                                                   'content_type_id':content_type_id.id,
                                                   'object_pk': object.id
                                                   }
                                )
    

@register.inclusion_tag('tree_comments/ajax_tree.html', takes_context=True)
def tree_comments_ajax(context, object):
    
    
    return {
        'action': get_post_url(object),
        'comments': Comment.objects.filter_for_object(object).filter(parent=None),
        'object':object,
        'user': context['user'],
    }
    
@register.simple_tag
def comments_post_url(object):
    return get_post_url(object)


def _human_datetime(var):
    import datetime, settings
    from pytils import numeral
#    numeral.choose_plural(amount, variants) 
    from django.utils.dateformat import format
    assert type(var) == datetime.datetime, "Wrong type %s " % type(var)
    now = datetime.datetime.today()
    #check today:
    if var.year==now.year and var.month==now.month and var.day==now.day:
        delta=now-var
        min = int(delta.seconds/60)
        if min==0:
            return unicode(ugettext("now"))
        if min<60:
            return ("%s" % min)+" "+ numeral.choose_plural(min,
                                        (ugettext("1 minute ago"),
                                         ugettext("2 minutes ago"), 
                                         ugettext("5 minutes ago"))
                                        )            
        if min>=60 and min<120:
            return unicode(ugettext("hour ago"))
        
        if min>=120 and min<=600:
            hour = int(min/60)
            return ("%s" % hour)+" "+ numeral.choose_plural(hour,
                                        (ugettext("1 hour ago"),
                                         ugettext("2 hours ago"), 
                                         ugettext("5 hours ago"))
                                        )        
        return format(var, settings.TIME_FORMAT)
    else:
        if var.year==now.year:
            if var.month==now.month:
                if var.day==now.day-1:
                    return format(var, ugettext("yesterday in H:i"))
                
                dd=now.day-var.day
                if dd<=7:
                    return ("%s" % dd)+" "+ numeral.choose_plural(dd,
                                                (ugettext("1 day ago"),
                                                 ugettext("2 days ago"), 
                                                 ugettext("5 days ago"))
                                                )
            
                
            return format(var, "d M.").lower()
    return format(var, "d M y").lower()

@register.filter_function
def human_datetime(var):
    return _human_datetime(var)