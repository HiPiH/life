# -*- coding: utf-8 -*-
from apps.config import property, registerConfig
from django.utils.translation import ugettext as _

__all__ = ('config',)

class Config(property.Container):
    
    _title = _(u'Blog config')
    authors_per_page = property.Int(30, title=_(u'кол-во авторов на страницу'))
    seo_title = property.String(default=u'Blog', title=_('SEO title'))
    seo_description = property.String(default=u'blog description', title=_('SEO description'))
    seo_keywords = property.String(default=u'rvca, site, blog', title=_('SEO keywords'))
    text_on_page = property.Text(default=u'....', title=_('Text on page'))
    
    posts_per_user_page = property.Int(3, title=_(u'кол-во постов на странице пользователя'))
    
config = registerConfig(Config())