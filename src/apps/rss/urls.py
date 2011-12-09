# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns
from apps.rss.views import EventsFeed,IdeaFeed
__author__ = 'Aleksey.Novgorodov'

urlpatterns = patterns('apps.rss.views',
    # INDEX PAGE
    (r'^events.xml$', EventsFeed()),
    (r'^idea.xml$', IdeaFeed())
)
