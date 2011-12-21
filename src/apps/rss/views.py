# -*- coding: utf-8 -*-  

from django.contrib.syndication.views import FeedDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib.syndication.views import Feed
from apps.events.models import Event

class EventsFeed(Feed):
    title = "Events"
    link = "/rss/events.xml"
#    description = "Updates on changes and additions to chicagocrime.org."

    def items(self):
        return Event.objects.filter(is_idea = False).order_by('-date_create')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
    


class IdeaFeed(Feed):
    title = "Events"
    link = "/rss/idea.xml"
#    description = "Updates on changes and additions to chicagocrime.org."

    def items(self):
        return Event.objects.filter(is_idea = True).order_by('-date_create')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
