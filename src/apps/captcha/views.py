# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse


from apps.captcha.util import render, generate

def captcha_image(request, captcha_id):
    """
    Generate and save image to response.
    """
    response = HttpResponse(mimetype='image/jpeg')
    render(captcha_id, response)
    return response

def get_new_image(req):
    captcha_id = generate()
    url = reverse('captcha_image', args=[captcha_id])
    return HttpResponse(content=simplejson.dumps({'captcha_id': captcha_id, 'src': url}))