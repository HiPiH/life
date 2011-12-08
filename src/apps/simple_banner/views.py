# coding: utf-8
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext
from django.db import models

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from apps.simple_banner.models import Banner


def redirect(req, id):
    banner = get_object_or_404(Banner, pk = id)
    return HttpResponseRedirect(banner.url)
