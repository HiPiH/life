# coding: utf-8

from django.utils.translation       import ugettext as _
from lib.shortcuts      import render_to
from datetime import date,timedelta

from processor import Processor
from apps.ajax_calendar import shortcuts

#class NewsCalendar(Processor):
#    
#    def get_linked_days(self, begin, end):
#        from apps.etpi.models import EconomyNews
#        news_days = EconomyNews.objects.actual().filter(date__gte=begin, date__lte=end).values_list('date')
#        days = []
#        for day in news_days:
#            day=day[0]
#            day = date(day.year, day.month, day.day)
#            if day not in days:
#                days.append(day)
#        return days


@render_to('ajax_calendar/test.html')
def test(req, cur_date, processor_type):
    out={}
    out['ajax_calendar'] = processor_type(req, cur_date)
    return out

@render_to('ajax_calendar/includes/ajax.html')
def ajax(req, cur_date, processor_type):
    out={}
    out['ajax_calendar'] = processor_type(req, cur_date)
    return out
