from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    author = models.ForeignKey(User, related_name="my_messages")
    to = models.ForeignKey(User, related_name="messages_to_me")
    create = models.DateTimeField(auto_now_add = True)
    text = models.TextField()
    is_delivered = models.BooleanField(default=False)
    
    def save(self):
        is_new = not self.id
        super(Message, self).save()
        if is_new and not self.is_delivered:
            self.to.im_incoming+=1  
            self.to.save()#TODO: optimize..... for update
    

#Add cache to User
User.add_to_class('im_incoming', models.PositiveIntegerField(default=0))