# -*- coding: utf-8 -*-
from apps.config import property, registerConfig
from django.utils.translation import ugettext as _
import datetime

__all__ = ('config',)

class Config(property.Container):
    
    _title = _(u'Site config')
    
    site_name = property.String(default=u'Site name', title=_('Site name'))
    slogan = property.String(default=u'Slogan', title=_('slogan'))
    site_description = property.Text(default=u'Description', title=_('Description'))
    
    seo_title = property.String(default=u'life.interzet.ru', title=_('SEO title for main page'))
    seo_description = property.Text(default=u'SEO description', title=_('SEO description for main page'))
    seo_keywords = property.String(default=u'seo, site, project', title=_('SEO keywords for main page'))
    
    title_main = property.String(default=u'Main title', title=_('Title on main page'))
    text_main = property.Text(default=u'main text', title=_('Text on main page'))
    text_footer = property.Text(default=u'text in footer', title=_('Text in footer'))
    text_contacts = property.Text(default=u'contacts', title=_('Our contacts'))
    
    copyrights = property.String(default=u'Copyrights', title=_('Copyrights'))
    site_email = property.String(default=u'info@example.com', title=_(u'Site email'))
    
config = registerConfig(Config())