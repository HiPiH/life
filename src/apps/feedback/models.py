# coding: utf-8

from django.db                      import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.contrib.auth.models import User
from datetime import datetime


class Feedback(models.Model):
    #название
    author = models.ForeignKey(User, blank=True, null=True)
    fio = models.CharField(max_length=255, verbose_name=_(u'ФИО'), blank=True)
    phone = models.CharField(max_length=255, verbose_name=_(u'Телефон'), blank=True)
    email = models.EmailField(verbose_name=_(u'E-Mail'), blank=True)
    text = models.TextField(verbose_name=_(u'Сообщение'))
    pub_date = models.DateTimeField(verbose_name=_(u'Дата сообщения'), blank=True, default=datetime.today())

    __unicode__ = lambda self: u"%s" % self.fio
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.pub_date = datetime.today()
        super(Feedback, self).save(*args, **kwargs)

    class Meta():
        verbose_name=_(u'Обратная связь')
        verbose_name_plural=_(u'Обратная связь')
        ordering = ('fio', )