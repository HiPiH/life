# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

app_label = _(u'config')

__all__ = ('register', 'autodiscover', 'aggregator',)


class TemplateConfigAccess(object):
    "Доступ к настройкам. Используется в шаблонах"
    
    def __init__(self, aggrigator):
        self.aggrigator=aggrigator
    
    def __getattr__(self, name):
        name=name.replace("__",".")
        for item in self.aggrigator.getList():
            if item['name']==name:
                return item['config']
        raise Exception("Not found  '%s' in\n '%s'" % (name, unicode( \
            map(lambda a:a['name'], self.aggrigator.getList()))))

class Aggregator(object):
    "Агригатор настроект - предназначен для работы с контейнерами настроек."
    
    def __init__(self):
        self.access=TemplateConfigAccess(self)
        self.configs=[]

    def getList(self):
        ret = []
        for config in self.configs:
            info={}
            info['name'] = unicode(config.__class__)
            info['title'] = config._title
            info['config'] = config
            info['get_absolute_url'] = config._get_absolute_url()
            ret.append(info)

        return ret
    
    def hasList(self):
        return len(self.configs) > 0
    
    def getClass(self, klass):
        for config in self.configs:
            if unicode(config.__class__)==klass:
                return config
        return None
    
    def register(self, config):
        self.configs.append(config)
        return config

aggregator = Aggregator()
registerConfig = aggregator.register

def autodiscover():
    from settings import INSTALLED_APPS
    for apps in INSTALLED_APPS :
        mod = __import__(apps, globals(), locals(), ['config'])
