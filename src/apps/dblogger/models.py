# coding: utf-8
from django.utils.translation       import ugettext_lazy as _
from django.db                      import models
__all__ = ('Log', 'LOG_EXCEPTION','LOG_WARNING','LOG_NOTICE','LOG_STRING')

import datetime 

LOG_EXCEPTION = 1
LOG_WARNING = 2
LOG_NOTICE = 3
LOG_STRING = 4

LOG_TYPE = (
    (LOG_EXCEPTION, _('LOG_EXCEPTION')),
    (LOG_WARNING, _('LOG_WARNING')),
    (LOG_NOTICE, _('LOG_NOTICE')),
    (LOG_STRING, _('LOG_STRING')),
)

#Log
class Log(models.Model):
    #date
    date = models.DateTimeField(verbose_name=_(u'date'))
    #type
    type = models.PositiveIntegerField(choices = LOG_TYPE, default=LOG_EXCEPTION, verbose_name=_(u'type'))
    #subject
    subject = models.CharField(max_length=255, verbose_name=_(u'subject'), blank=True)
    #content
    content = models.TextField(verbose_name=_(u'content'), blank=True)
    
    __unicode__ = lambda self: self.subject

    class Meta():
        verbose_name=_(u'Log')
        verbose_name_plural=_(u'Log')
        ordering = ('-date',)
        
    def save(self):
        if not self.id:
            self.date = datetime.datetime.today()
        super(Log, self).save()
