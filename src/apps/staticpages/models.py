# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from pytils import translit
from settings import SITE_NAME
from apps.utils.middleware import threadlocals
from django.template.loader         import render_to_string

__all__ = ('Page', )

# Create your models here.
class Page(models.Model):
    title = models.CharField(_('title'), max_length=200)
    address = models.SlugField(_('address'), blank=True, unique=True) # unique=True, - exclude for Language
    content = models.TextField(_('content'))
    
    published = models.BooleanField(_('published'), default=True)
    
    #Метатэги
    seo_title       = models.CharField(_('title for SEO'), max_length=255, blank=True)
    seo_keywords    = models.CharField(_('keywords for SEO'), max_length=255, blank=True)
    seo_description = models.CharField(_('description for SEO'), max_length=255, blank=True)
    
    __unicode__ = lambda self: u'%s' % self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('staticpages_page', [self.address])
    
    def save(self, *args, **kwargs):
        if self.address == '':
            self.address = translit.slugify(self.title)[:50]
        super(Page, self).save(*args, **kwargs)
    
    ########################################################################################################
    # IMAGE PREVIEW
    def address_link(self):
        out={}
        out['self'] = self if self.address else None
        out['base_url'] = '/pages/'
        return render_to_string('admin/interfaces/staticpages/getlink.html', out)
            
    address_link.allow_tags = True
    address_link.short_description = _('link')
    
    # PUBLISHED custom admin column
    def my_tag_published(self):
        out = {}
        out['name'] = 'published'
        out['self'] = self
        out['parameter'] = self.published
        return render_to_string('admin/interfaces/checkbox.html', out)
                
    my_tag_published.allow_tags = True
    my_tag_published.short_description = _('published')
    
    # DELETE TAG
    def my_tag_delete(self):
        out={}
        out['id'] = self.id
        return render_to_string('admin/interfaces/button_delete.html', out)
                
    my_tag_delete.allow_tags = True
    my_tag_delete.short_description = _('Delete?')
    ########################################################################################################
    
    class Meta:
        verbose_name        = _('page')
        verbose_name_plural = _('pages')

