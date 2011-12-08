# -*- coding: utf-8 -*-
# Original: http://django-pantheon.googlecode.com/svn/trunk/pantheon/supernovaforms/

from django import forms as forms
from django.core.urlresolvers import reverse

from captcha import util

class ImageWidget( forms.Widget ):
    """
    Widget for rendering captcha image.
    """

    def render( self, name, value, attrs=None ):
        return forms.HiddenInput().render( name, value ) + \
               u'<img id="%s" src="%s"/><img style="cursor: hand; cursor: pointer;" src="/media/i/view-refresh.png" onclick="onRefreshClick(\'%s\',\'%s\')">' \
               % (name[:-2]+'_C', value, name[:-2], reverse('captcha.views.get_new_image'))


class CaptchaWidget( forms.MultiWidget ):
    """
    Multiwidget for rendering captcha field.
    """

    def __init__(self, attrs = None):
        widgets = ( forms.HiddenInput(), ImageWidget(), forms.TextInput())
        super( CaptchaWidget, self ).__init__( widgets, attrs )
   

    def format_output(self, widgets):
        return u'<div class="captcha">%s<div class="captcha-image">%s</div><div class="captcha-input">%s</div></div>' % (widgets[0], widgets[1], widgets[2])
   

    def decompress(self, value):
        captcha_id = util.generate()
        url = reverse('captcha.views.captcha_image', args=[captcha_id])
        return (captcha_id, url, '')


    def render(self, name, value, attrs=None):
        # None value forces call to decompress
        # which will generate new captcha
        return super(CaptchaWidget, self).render(name, None, attrs)
   

class CaptchaField(forms.Field):
    """
    Captcha field.
    """

    widget = CaptchaWidget

    def __init__(self, *args, **kwargs):
        super(CaptchaField, self).__init__(*args, **kwargs)
        self.label = u'Код подтверждения'
        self.help_text = u'Пожалуйста, введите слово, которые вы видите на картинке'


    def clean(self, values):
        """
        Test the solution
        """
        
        id, url, solution = values
        if not util.test_solution(id, solution):
            raise forms.ValidationError(u'Введен неверный код подтверждения')
        return values
