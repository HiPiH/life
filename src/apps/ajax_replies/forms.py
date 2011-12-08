# -*- coding: utf-8 -*-

from django                   import forms
from django.utils.translation import ugettext_lazy as _
from apps.utils.forms              import CustomForm, CustomModelForm

class AddReplyForm ( CustomForm ):
    body = forms.CharField ( widget = forms.Textarea, label = _( u"введите текст комментария" ) )