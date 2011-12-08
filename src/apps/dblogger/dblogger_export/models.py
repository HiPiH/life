# coding: utf-8
from django.utils.translation       import ugettext_lazy as _
from django.db                      import models
__all__ = ('Log', )


#Log
class Log(models.Model):
    #date
    date = models.DateTimeField(verbose_name=_(u'date'))
    #type
    type = models.PositiveIntegerField(help_text=u'exception, warning, notice, log', default=1, verbose_name=_(u'type'))
    #subject
    subject = models.CharField(max_length=255, verbose_name=_(u'subject'), blank=True)
    #content
    content = models.TextField(verbose_name=_(u'content'), blank=True)

    class Meta():
        verbose_name=_(u'Log')
        verbose_name_plural=_(u'Log')
        ordering = ('-date', )
