# -*- coding: utf-8 -*-
# Original: http://django-pantheon.googlecode.com/svn/trunk/pantheon/supernovaforms/

import sha
import random
import os.path

#TODO: make smart import: PIL, Image etc
import Image
import ImageFont
import ImageDraw

from django.conf import settings

from utils.captcha.threadlocals import get_request


#TODO: find similar function in stdlib or django utils
def random_word(size=6):
    """
    Generate random alphanumeric word.
    """
    
    chars = "0123456789"
    return ''.join(random.choice(chars) for x in xrange(size))


def solutions():
    """
    Return solutions list from session
    """

    session = get_request().session
    if not 'captcha_solutions' in session:
        session['captcha_solutions'] = {}
    return session['captcha_solutions']


def generate():
    """
    Generate random solution and save it in session.
    """

    solution = random_word()
    captcha_id =  sha.new(solution + settings.SECRET_KEY).hexdigest()
    solutions()[captcha_id] = solution
    # http://www.djangoproject.com/documentation/sessions/#when-sessions-are-saved
    get_request().session.modified = True
    return captcha_id


def test_solution(captcha_id, solution):
    return solution == solutions().get(captcha_id, None)


def render(captcha_id, output):
    """
    Generate image and save it to output stream.
    """

    solution = solutions().get(captcha_id, 'foobar')
    fgcolor = 0xffffff
    bgcolor = 0x000000
    linecolor = 0xfafafa
    font = ImageFont.truetype(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'frizzed.ttf'), 25)
    dim = font.getsize(solution)
    img = Image.new('RGB', (dim[0] + 20, dim[1] + 10), bgcolor) 
    draw = ImageDraw.Draw(img)
    draw.text((10, 5), solution, font=font, fill=fgcolor)
    draw.line((0, 4, img.size[0], 4,), fill=linecolor)
    draw.line((0, 32, img.size[0], 4,), fill=linecolor)
    draw.line((0, 4, img.size[0], 32,), fill=linecolor)
    draw.line((0, 32, img.size[0], 32,), fill=linecolor)
    img.save(output, format='JPEG')
