# coding: utf-8

from django.db                      import models
from django.utils.translation import ugettext_lazy as _, ugettext



class Banner(models.Model):
    #название
    name = models.CharField(max_length=255, verbose_name=_(u'Название'), blank=True)
    image = models.ImageField(upload_to='upload/', verbose_name=_(u'Изображение'), blank=True)
    published = models.BooleanField(verbose_name=_(u'Опубликовать'), default=True)
    url = models.URLField(verbose_name=u"URL")

    __unicode__ = lambda self: u"%s" % self.name
    

    class Meta():
        verbose_name=_(u'Банер')
        verbose_name_plural=_(u'Банер')
