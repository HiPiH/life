from apps.messages.models   import UsersCommunication
from django.db.models       import Q

class CPMessages():

    def __init__(self, req):
        self.req=req
        
    def count_new(self):
        if not self.req.user.is_authenticated():
            return 0
        AuthorOrRecipientNewMessages = Q(author = self.req.user, count_mes_a_new__gt=0) | Q(recipient = self.req.user, count_mes_r_new__gt=0)
        communication = UsersCommunication.objects.filter(AuthorOrRecipientNewMessages)
        summ_new = 0
        for c in communication:
            if c.author == self.req.user:
                summ_new = summ_new + c.count_mes_a_new
            else:
                summ_new = summ_new + c.count_mes_r_new
        return summ_new
        

def cp_messages(request):
    
    return {
        'cp_messages': CPMessages(request),
    }