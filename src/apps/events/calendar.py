
from apps.ajax_calendar.processor import Processor
from django.core.urlresolvers       import reverse
from django.db.models import Q

from datetime import date, timedelta

def day_iterator(begin, end):
        cur = begin
        while cur<end:
            yield cur
            cur=cur+timedelta(1)


class EventsCalendar(Processor):

    calendar_view_name = 'events_ajax_calendar'
    
    content_view_name = 'events_list'
    
    def day_url(self, date):
        if not self.content_view_name:
            raise NotImplementedError, "define 'content_view_name' in your Calendar processor"
        return reverse(self.content_view_name, kwargs={'date':date,'date2':date,})
    
    
    def get_linked_days(self, begin, end):
        from apps.events.models import Meeting 
        news_days = Meeting.objects.actual().filter(
                                         begin__lte=end, end__gte=begin
                                         ).values_list('begin', 'end','id')
        days = []
        for day in news_days:
            for d in day_iterator(day[0], day[1]):
                d = date(d.year, d.month, d.day)
                if d not in days:
                    days.append(d)
        return days
