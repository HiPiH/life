
from apps.events.models import *
from apps.events.calendar import EventsCalendar

class CPEvents(object):
    
    def __init__(self, req):
        self.req = req
        
    def has_new_invite(self):
        if self.req.user.is_authenticated():
            return EventInvite.objects.filter(user=self.req.user, accepted=None)
        return []
    
    def new_invite_count(self):
        return len(self.has_new_invite())

    
    def has_new_friends(self):
        if self.req.user.is_authenticated():
            return self.req.user.get_new_friends()
        return []
    
    def new_friends_count(self):
        return len(self.has_new_friends)

    
    
    def top5_idea(self):
        return Event.objects.filter(is_idea = True).order_by('-idea_rang', '-id')[:5]
    

    
def cp_events(req):
    return {'cp_events': CPEvents(req)}


def ajax_calendar(req):
    return {'ajax_calendar':EventsCalendar(req)}
