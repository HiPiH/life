# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns
from apps.rss.views import EventsFeed,IdeaFeed
from django.conf.urls.defaults import *

urlpatterns = patterns('apps.rss.views',
    # INDEX PAGE
    url(r'^events.xml$', EventsFeed(),name='rss_events'),
    url(r'^idea.xml$', IdeaFeed())
)
