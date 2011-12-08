

class CPIM():
    
    def __init__(self, req):
        self.req=req
        
    def not_delivered_messages_count(self):
        if self.req.user.user.is_authenticated():
            return self.req.user.im_incoming
        return 0

    
def cp_im(req):

    return {'cp_im':CPIM(req)}