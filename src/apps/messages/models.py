#coding: utf-8
from django.utils.translation       import ugettext_lazy as _
from django.db                      import models
from django.contrib.auth.models     import User
from django.template.loader         import render_to_string

import datetime

FolderDefault        = 0
FolderFavorites      = 1    
FolderBlackList      = 2
FolderDeleted        = 3
 
    
FOLDERS = (
    (FolderDefault, _(u'Основная папка')),
    (FolderFavorites, _(u'Избранные')),
    (FolderBlackList, _(u'Черный список')),
    (FolderDeleted, _(u'Удаленные')),
)

class UsersCommunication(models.Model):
    author           =  models.ForeignKey(User, verbose_name=_('author'), related_name='users_communication_author')
    recipient        =  models.ForeignKey(User, verbose_name=_('recipient'), related_name='users_communication_recipient')
    count_mes_a      =  models.IntegerField(_('count author messages'), default=0, editable=False)
    count_mes_a_new  =  models.IntegerField(_('count author new messages'), default=0, editable=False)
    count_mes_r      =  models.IntegerField(_('count recipient messages'), default=0, editable=False)
    count_mes_r_new  =  models.IntegerField(_('count recipient new messages'), default=0, editable=False)
    folder_a         =  models.PositiveSmallIntegerField(_('folder author'), db_index=True, choices=FOLDERS, default=FolderDefault)
    folder_r         =  models.PositiveSmallIntegerField(_('folder author'), db_index=True, choices=FOLDERS, default=FolderDefault)
    date_create      =  models.DateTimeField(_(u'create date'), auto_now_add=True)
    date_changed     =  models.DateTimeField(_(u'last change date'), auto_now=True)
    
    def apponent(self):
        from apps.utils.middleware.threadlocals import get_current_user
        user = get_current_user()
        if user:
            return self.recipient if user==self.author else self.author
        return None
    
    def my_message_count(self):
        from apps.utils.middleware.threadlocals import get_current_user
        user = get_current_user()
        if user:
            return self.count_mes_a if user==self.author else self.count_mes_r
        return None

    def my_new_message_count(self):
        from apps.utils.middleware.threadlocals import get_current_user
        user = get_current_user()
        if user:
            return self.count_mes_a_new if user==self.author else self.count_mes_r_new
        return None
        
        
    
    def __unicode__(self):
        return u'%s and %s' % (self.author, self.recipient)
    
    class Meta():
        verbose_name        = _(u'UsersRelation')
        verbose_name_plural = _(u'UsersRelations')
        ordering = ('-id', )
        
        
class MessageCommunication(models.Model):
    communication_to  =  models.ForeignKey(UsersCommunication, verbose_name=_('to users communications'))
    recipient         =  models.ForeignKey(User, verbose_name=_('recipient'), related_name='message_communication_recipient')
    date_create       =  models.DateTimeField(_('create date'), auto_now_add=True)
    date_changed      =  models.DateTimeField(_('last change date'), auto_now=True)
    text              =  models.TextField(_('text'))
    is_read           =  models.BooleanField(_('is read'), default=False, db_index=True)

    def __unicode__(self):
        return u'%s and %s. Message for %s.' % (self.communication_to.author, self.communication_to.recipient, self.recipient)
    
    def save(self):
        if not self.id:
            self.communication_to.count_mes_r += 1
            self.communication_to.count_mes_a += 1
            if self.communication_to.recipient == self.recipient:
                self.communication_to.count_mes_r_new += 1
            else:
                self.communication_to.count_mes_a_new += 1
            self.communication_to.save()
        super(MessageCommunication, self).save()
    
    class Meta():
        verbose_name        = _(u'Message')
        verbose_name_plural = _(u'Messages')
        ordering = ('-id', )