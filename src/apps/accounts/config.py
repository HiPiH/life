# -*- coding: utf-8 -*-
from django.utils.translation   import ugettext_lazy as _
from apps.config import property, registerConfig
import datetime

__all__ = ('config',)


NEW_USERS = datetime.datetime.today() - datetime.timedelta(3)

class Config(property.Container):
    _title = _('Accounts config')
    
    validation_new_users = property.Bool(default=False,title=_('Validation new users'))
    notification_admin = property.Bool(default=False,title=_('Notification admins about new users'))
    text_for_registration_page = property.Text(default=_(u"Пожалуйста, зарегистрируйтесь."), title=_('Text on registration page'))
    text_for_forgot_password_page = property.Text(default=_(u"Введите адрес электронной почты для восстановления пароля..."), title=_('Text on forgot password page'))
    text_for_validation_page = property.Text(default=_(u"На указанный адрес электронной почты выслан код для восстановения пароля..."), title=_('Text on validation page'))
    text_for_login_page = property.Text(default=_("Please login..."), title=_('Text on login page'))
    text_for_profile_page = property.Text(default=_("This is your profile..."), title=_('Text on profile page'))
#    avatar_image_width = property.Int(default=50, title=_('Avatar image width (pixel)'))
#    avatar_image_height = property.Int(default=60, title=_('Avatar image height (pixel)'))
    
    friends_per_page = property.Int(default=20, title=_('Friends per page'))

config = registerConfig(Config())
