# coding: utf-8
from django import forms
from apps.feedback.models import Feedback
from apps.utils.forms import CustomModelForm
from django.utils.translation import ugettext_lazy as _, ugettext

class FeddbackForm(CustomModelForm):
    
    fio = forms.CharField(max_length=255, label=_(u'ФИО'), required=True)
#    phone = forms.CharField(max_length=255, label=_(u'Телефон'), required=True)
    email = forms.EmailField(label=_(u'E-Mail'), required=True)
    
    
    class Meta:
        model = Feedback
        fields = ['fio','email','phone', 'text', ]


class FeddbackAuthForm(CustomModelForm):
    
    class Meta:
        model = Feedback
        fields = ['text',]    