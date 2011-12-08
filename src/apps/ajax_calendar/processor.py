
__all__=('Processor', 'Day',)

from datetime import date, timedelta
from django.core.urlresolvers       import reverse

import calendar
import types
import time

SESSION_ID = 'ajax_calendar'

class Day(object):
    
    def __init__(self, date, linked, processor):
        self.date=date
        self.linked=linked
        self.processor = processor
    
    def is_actual(self):
        return True
    
    def is_today(self):
        return date.today()==self.date
    
    def is_day_off(self):
        return self.date.weekday() in [5,6]
    
    def is_linked(self):
        return self.linked
    
    def is_selected(self):
        return self.processor.is_selected(self.date)
    
    def url(self):
        return self.processor.day_url(self.date)

    
class NoDay(Day):

    def is_linked(self):
        return False

    def is_actual(self):
        return False
    
    def url(self):
        return "#"
    
    
class DaysRow(object):
    
    def __init__(self):
        self.days=[]
    
    def append(self, day):
        self.days.append(day)
    

class Processor(object):
    
    calendar_view_name = 'ajax_calendar_test'
    content_view_name = None  #"define 'content_view_name' in your Calendar processor"
    
    def day_url(self, date):
        if not self.content_view_name:
            raise NotImplementedError, "define 'content_view_name' in your Calendar processor"
        return reverse(self.content_view_name, kwargs={'date':date,})
    
    def is_selected(self, date):
        if not self.date and not self.date2:
            return False
        if self.date and date<self.date:
            return False
        if self.date2 and date>self.date2:
            return False
        return True
        
    
    def __init__(self, req, cur_date=None, use_session=True):
        self.req=req
        
        self.date = self.date2 = None
        if hasattr(self.req,'events_filter_date') and self.req.events_filter_date:
            self.date = date(*time.strptime(self.req.events_filter_date, "%Y-%m-%d")[:3])

        if hasattr(self.req,'events_filter_date2') and self.req.events_filter_date2:
            self.date2 = date(*time.strptime(self.req.events_filter_date2, "%Y-%m-%d")[:3])
        
                    
        if not cur_date:
            if use_session and SESSION_ID in self.req.session:
                cur_date = self.req.session[SESSION_ID]
            
            if not cur_date:
                cur_date = date.today()
            
        if isinstance(cur_date, (str, unicode)):
            cur_date = date(*time.strptime(cur_date, "%Y-%m-%d")[:3])
        self.cur_date = cur_date        
        
        if use_session:
            self.req.session[SESSION_ID]=self.cur_date
        
    def get_linked_days(self, begin, end):
        raise NotImplementedError, "Not implemented error"
    
    def first_month_day(self):
        return date(self.cur_date.year, self.cur_date.month, 1)
    
    def next_month(self):
        normal_day = self.first_month_day()
        day1, ndays = calendar.monthrange(normal_day.year, normal_day.month)
        return normal_day+timedelta(ndays)
    
    def next_month_url(self):
        return reverse(self.calendar_view_name, args=(self.next_month(),))
    
    def prev_month(self):
        last_day = self.first_month_day() - timedelta(1)
        return date(last_day.year, last_day.month, 1)
    
    def prev_month_url(self):
        return reverse(self.calendar_view_name, args=(self.prev_month(),))

    def today_month(self):
        now = date.today()
        return date(now.year, now.month, 1)
    
    def today_month_url(self):
        return reverse(self.calendar_view_name, args=(self.today_month(),))
    
    def month(self):
        day1, ndays = calendar.monthrange(self.cur_date.year, self.cur_date.month)
        
        begin = cur_week = date(self.cur_date.year, self.cur_date.month, 1)
        cur_week = cur_week - timedelta(cur_week.weekday())
        ret = []
 
        linked_days = self.get_linked_days(begin, begin+timedelta(ndays-1)) 
        
        for row_num in range(5):
            row = DaysRow()
            for day_num in range(7):
                cur_day = cur_week + timedelta(day_num)
                day_class = Day if cur_day.month==self.cur_date.month else NoDay
                row.append(day_class(cur_day, cur_day in linked_days, self))                            
            ret.append(row)    
            cur_week=cur_week+timedelta(7)
        return ret
        
    def days_range(self, begin, end):
        cur = begin
        while cur<end:
            yield cur
            cur=cur+timedelta(1)
#        
#    def month_context(self, req):
#        out={}
#        
#        out['ajax_calendar'] = self.month()
#        
#        return out
    
