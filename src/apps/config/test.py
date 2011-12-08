# -*- coding: utf-8 -*-
from django.utils.translation   import ugettext_lazy as _
from apps.config import property, registerConfig

__all__ = ('config',)

def testOnChange(container, oldValue, newValue):
    print "old value=", oldValue
    print "new value=", newValue
#    
#    print container.specModuleLimit
#    print dir(container.specModuleLimit)


class Config(property.Container):
    
    _title = _('Goods config')
    specModuleLimit = property.Int(default=10, title=_('News limit in special module'), onChange=testOnChange)
    text_for_list_page = property.Text(default=u"", title=_('Text for list page'))
    seo_title_for_list = property.String(default=u"", title=_('SEO title for list page'))
    seo_description_for_list = property.String(default=u"", title=_('SEO description for list page'))
    seo_keywords_for_list = property.String(default=u"", title=_('SEO keywords for list page'))
    limitOnList = property.Int(default=10, title=_('News limit in list page'))

    
config = registerConfig(Config())