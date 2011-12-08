# coding: utf-8
from apps.config import property, registerConfig
from django.utils.translation import ugettext as _

__all__ = ('config',)

class Config(property.Container):
    _title = _(u'настройки событий')
    
#    title_main = property.String(default=u'Main title', title=_(u'Заголовок на главную страницу'))
#    text_main = property.Text(default=u'main text', title=_(u'Текст на главной страницы'))
    
    events_per_page = property.Int(10, title=_(u'кол-во событий на страницу'))
    photo_per_page = property.Int(20, title=_(u'кол-во фотографий на страницу'))
    events_per_user_page = property.Int(3, title=_(u'событий на странице пользователя'))
    friends_per_user_page = property.Int(30, title=_(u'друзей на странице пользователя'))
    friends_per_page = property.Int(30, title=_(u'друзей на страницу'))
    comments_per_page = property.Int(30, title=_(u'комментариев на страницу'))
    
    idea_processing_amount = property.Int(1, title=_(u'Кол-во обрабатываемых идей за один шаг'))
#    city_in_page = property.Int(20, title=_(u'кол-во регионов на страницу'))
#    photos_per_page = property.Int(8, title=_(u'кол-во фотографий на странице'))
#    reports_per_page = property.Int ( 10, title = _(u'кол-во отчетов на странице') )
#    press_per_page = property.Int ( 10, title = _(u'кол-во публикаций на странице') )
#    main_region_page = property.Text(default=u'Текст редактируеться в системе администрирования', title=_(u'Текст раздела регоны'))
#    main_services_page = property.Text ( default = u'Текст редактируеться в системе администрирования', title = _(u'Текст раздела услуги') )
#    feedback_email = property.String(default=u'feedback@example.com', title=_(u'E-mail для обратной связи'))
    
config = registerConfig(Config())