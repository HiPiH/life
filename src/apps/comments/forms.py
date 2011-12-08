from django import forms
from django.utils.translation import ugettext_lazy as _

class Textarea(forms.Textarea):
    def __init__(self, attrs=None):
        super(forms.Textarea, Textarea).__init__(self)
        if attrs:
            self.attrs.update(attrs)

class CommentForm(forms.Form):
    body = forms.CharField(label=_(u'body').capitalize(), widget=Textarea({'style': "width: 100%", 'rows': '5'}))
    content_type = forms.CharField(widget=forms.HiddenInput())
    object_id = forms.CharField(widget=forms.HiddenInput())
    next = forms.CharField(widget=forms.HiddenInput())

class RecallForm(forms.Form):
    body = forms.CharField(label=_(u'body').capitalize(), widget=Textarea({'style': "width: 100%", 'rows': '5'}))
    content_type = forms.CharField(widget=forms.HiddenInput())
    object_id = forms.CharField(widget=forms.HiddenInput())
    next = forms.CharField(widget=forms.HiddenInput())
