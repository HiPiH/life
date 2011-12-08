# coding: utf-8
from apps.utils.shortcuts import render_to
from apps.feedback.forms import FeddbackForm, FeddbackAuthForm
from django.core.urlresolvers import reverse
from apps.utils.mail import send_mail
from django.utils.translation import ugettext
from django.template.loader import render_to_string
from django.template.context import RequestContext
from django.db import models
from django.contrib.auth.models import User

from settings import SEND_FROM_EMAIL
from django.http import HttpResponseRedirect



@render_to("feedback/form.html")
def form(req):
    out={}
    feedback_form = FeddbackAuthForm if req.user.is_authenticated() else FeddbackForm
    if req.POST:        
        out['form'] = form = feedback_form(req.POST)
        if form.is_valid():
            if req.user.is_authenticated():
                form.instance.author=req.user
            form.save()
            #send E-Mail
            emails = User.objects.filter(models.Q(is_superuser=True) | models.Q(is_staff = True) ).values_list('email')
            out['feedback'] = form.instance
            
            send_mail(ugettext('New feedback'),
                      render_to_string('feedback/email.html',out, context_instance = RequestContext(req)),
                      SEND_FROM_EMAIL,
                      emails,
                      fail_silently=False,
                      content_subtype='html'
                      )              
            req.flash.notice = ugettext(u'Ваше сообщение успешно отправлено')
            return HttpResponseRedirect(reverse("feedback_form"))
    else:
        out['form'] = feedback_form()
    return out