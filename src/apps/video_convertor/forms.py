# coding: utf-8
from django import forms
from apps.video_convertor.models import Video
import random

syms = '0123456789abcdefghijklmnopqrstuvwxyz'

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('video', )
    
    def save(self, *args, **kwargs):
        self.cleaned_data['video'].name = ''.join(random.sample(syms, 16))
        return super(VideoForm, self).save()