# coding: utf-8
from datetime import time as t, date as d, datetime as dt
from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.db.models import permalink
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from apps.utils.managers import PublishedManager

class Recall(models.Model):
    author = models.ForeignKey(User, verbose_name=_(u'author'), related_name='recalls')
    pub_date = models.DateTimeField(_(u'publishing date'), editable=False, auto_now = True)
    body = models.TextField(_(u'body'))
    published = models.BooleanField(_(u'published'), default=False)
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    object = generic.GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        verbose_name        = _(u'recall')
        verbose_name_plural = _(u'recalls')
        
    def get_comment_on(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)
    
    def __unicode__(self):
        return "%s: %s" % (self.author, self.body[:20])
    
    def delete(self):
        if self.content_type and self.object_id:
            obj = self.get_comment_on()
            if hasattr(obj, 'recalls_count'):
                obj.recalls_count -= 1
                obj.save()
        super(Recall, self).delete()
    
    
    def save(self):
        if not self.id and self.content_type and self.object_id:
            obj = self.get_comment_on()
            if hasattr(obj, 'recalls_count'):  
                obj.recalls_count += 1
                obj.save()
            if hasattr(obj, 'last_recall_date'):
                obj.last_recall_date = datetime.now()
                obj.save()
        super(Recall, self).save()
    
    #admin methods
    def commented_obj_link(self):
        return render_to_string('comments/commentedobj.html', {'content_type': self.content_type,
                                                               'addr': self.get_comment_on().get_absolute_url(),
                                                               'text': self.get_comment_on()})
    
    commented_obj_link.allow_tags = True
    commented_obj_link.short_description = _('theme')
    commented_obj_link.admin_order_field = 'content_type'


class CommentNode(models.Model):
    # Comment fields
    author = models.ForeignKey(User, verbose_name=_(u'author'), related_name='comments')
    pub_date = models.DateTimeField(_(u'publishing date'), editable=False, default=datetime.now)
    body = models.TextField(_(u'body'))
    published = models.BooleanField(_(u'published'), default=False)
    on_comment = models.PositiveIntegerField(default=0, editable=False)
    path = models.TextField(editable=False, default='')
    indent = models.PositiveIntegerField(default=0, editable=False)
    ip_address  = models.IPAddressField(_('IP address'), blank=True, null=True)
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name        = _(u'comment')
        verbose_name_plural = _(u'comments')

    def __unicode__(self):
        return "%s: %s" % (self.author, self.body[:20])

    def save(self):
        if self.body:
            self.body = self.body.strip()
        #if not self.id:
            # Get the object being commented on
            #comment_on = self.content_type.get_object_for_this_type(pk=self.object_id)
            #self.comment_num = comment_on.comments_count
            #comment_on.comments_count += 1
            #comment_on.save()
        super(CommentNode, self).save()
        if self.on_comment:
            cm = CommentNode.objects.get(pk=self.on_comment)
            self.path = u'%s_%0.9d' % (cm.path, self.id)
        else:
            self.path = u'%0.9d' % self.id
        self.indent = len(self.path.split(u'_'))-1
        super(CommentNode, self).save()
    
    def delete(self):
        child_comments = self.get_child_comments()
        for li in child_comments:
            li.delete()
        super(CommentNode, self).delete()
    
    def get_child_comments(self):
        return CommentNode.objects.filter(path__startswith=self.path).exclude(pk=self.id)
    
    def get_absolute_url(self):
        return '%s#c%s' % (self.object.get_absolute_url(), self.id)

    def get_comment_on(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)
    
    #admin methods
    def commented_obj_link(self):
        return render_to_string('comments/commentedobj.html', {'content_type': self.content_type,
                                                               'addr': self.get_comment_on().get_absolute_url(),
                                                               'text': self.get_comment_on()})
    
    commented_obj_link.allow_tags = True
    commented_obj_link.short_description = _('theme')
    commented_obj_link.admin_order_field = 'content_type'
    
    def author_control(self):
        return render_to_string('comments/author_control.html', {'author': self.author,
                                                                 'comment': self})
    
    author_control.allow_tags = True
    author_control.short_description = _('author')
    author_control.admin_order_field = 'author'

    def ban_control(self):
        return render_to_string('comments/ban_control.html', {'comment': self})
    
    ban_control.allow_tags = True
    ban_control.short_description = u"Удаление"

    def ip_control(self):
        from apps.accounts.models import is_ip_banned
        return render_to_string('comments/ip_control.html', {'comment': self,
                                                             'banned': is_ip_banned(self.ip_address)})
    
    ip_control.allow_tags = True
    ip_control.short_description = _('IP address')
    ip_control.admin_order_field = 'ip_address'
