# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

#from apps.tree_comments.notify import CommentsNotify
#from apps.utils.text_parser import smart_truncate

def smart_truncate(content, length=100, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix

import datetime, settings

__all__ = ('Comment',)

class CommentManager(models.Manager):
    
    def filter_for_object(self, object):
        ct = ContentType.objects.get_for_model(type(object))        
        return self.filter(content_type = ct, object_pk = object.pk)

class Comment(models.Model):
    objects = CommentManager()
    
    # Content-object field
    content_type   = models.ForeignKey(ContentType)    
    object_pk      = models.PositiveIntegerField(_('Event Id'))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    #Comment
    author = models.ForeignKey(User)
    parent = models.ForeignKey('Comment', null=True, blank=True, default=None)
        
    text = models.TextField(_('Comment'))
    formated_text = models.TextField(editable = False) 
    
    submit_date = models.DateTimeField(_('Submit date'), default = datetime.datetime.now)
    ip_address  = models.IPAddressField(_('IP address'), blank=True, null=True)
        
    is_removed  = models.BooleanField(_('is removed'), default=False,
                    help_text=_('Check this box if the comment is inappropriate. ' \
                                'A "This comment has been removed" message will ' \
                                'be displayed instead.'))
    
    comments_count = models.PositiveIntegerField(default=0, editable=False)
    
#    rang = models.IntegerField(_("Comment's rang"), default=0)
    
    __unicode__ = lambda self: self.text
    
    class Meta():
        ordering = ('submit_date',)
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        
    def __iter__(self):
        for comment in Comment.objects.filter(parent = self).order_by('submit_date'):
            yield comment

    def get_absolute_url(self):
        return "%s#%s" % (self.content_object.get_absolute_url(), self.get_anchor())   
    
    def get_anchor(self):
        if self.parent:
            return self.parent.get_anchor()+"%s_" % self.id
        return "%s_" % self.id
    
    def delete(self):
        if self.parent:
            self.parent.comments_count-=1
            self.parent.save()
        #check object field
        if hasattr(self.content_object, 'comments_count'):
            self.content_object.comments_count-=1
            self.content_object.save()
        
    
    def save(self, *args, **kwargs):
        is_new = not self.id   
        if not self.id: #NEW
            if self.parent:
                self.parent.comments_count+=1
                self.parent.save()
            #check object field
            if hasattr(self.content_object, 'comments_count'):
                self.content_object.comments_count+=1
                self.content_object.save()
            
        super(Comment, self).save(*args, **kwargs)        

#        if is_new:
#            #Send Notification
#            if self.parent:                
#                if self.author!=self.parent.author:
#                    CommentsNotify.new_comment_for_comment([self.parent.author], self.get_absolute_url(),
#                                        type_name = self.content_object._meta.verbose_name,
#                                        title = unicode(self.content_object),
#                                        comment = smart_truncate(unicode(self.text), 500),
#                                        author = self.author.get_full_name()
#                                    )
#            else: #new comment for comment
#                if hasattr(self.content_object, 'author'):
#                    CommentsNotify.new_comment([self.content_object.author], self.get_absolute_url(),
#                                        type_name = self.content_object._meta.verbose_name,
#                                        title = unicode(self.content_object),
#                                        comment = smart_truncate(unicode(self.text), 500),
#                                        author = self.author.get_full_name()
#                                    )        