from django.contrib.auth.decorators import login_required
from apps.utils.shortcuts import render_to
from apps.instant_messages.ajax import IMAjax

ajax = IMAjax()

@login_required
@render_to("instant_messages/window.html")
def window(req):
    out={}
    return out