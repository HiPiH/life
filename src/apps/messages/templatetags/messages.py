# coding:utf-8
import sys
from django                          import template
from django.core.urlresolvers        import reverse
from django.utils.translation        import ugettext_lazy as _
from django.contrib.auth.models      import User
from django.db.models                import Q
from django.template.loader          import render_to_string
from django.contrib.auth.decorators  import login_required
from apps.messages.models            import UsersCommunication 

register = template.Library()
  
@register.simple_tag
def tag_messages_with(now_username=None, with_username=None):
    out = {}
    out['now_user']  = now_user  = User.objects.get(username='%s' % now_username)
    out['with_user'] = with_user = User.objects.get(username='%s' % with_username)
    if now_user == with_user:
        return u'Error: пользователи одинаковые'
    AuthorOrRecipient = Q(author = now_user, recipient = with_user) | Q(author = with_user, recipient = now_user)
    try:
        out['communication'] = UsersCommunication.objects.get(AuthorOrRecipient)
    except:
        return render_to_string('messages/template_tags/user_communication_new.html', out)
    
    return render_to_string('messages/template_tags/user_communication.html', out)