# coding: utf-8
from apps.accounts.config import config
from apps.accounts.image import copyFile, smart_thumbEx
from apps.events.models import Metro, RangHistory
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.db.models import Avg
import datetime
import settings


__all__ = ('SEX','MEN_SEX','WOMAN_SEX','Friends','UsersAvatars')

# МОДЕЛЬ ХРАНИТ СТАНДАРТНЫЕ АВАТАРКИ - ЗАКАЧЕННЫЕ АДМИНОМ И ПОЛЬЗОВАТЕЛЯМИ

AVATAR_FROM_ADMIN  = 0  #закачал админ
AVATAR_FROM_USERS  = 1  #закачал пользователь
 
    
WHO_UPLOADS = (
    (AVATAR_FROM_ADMIN, _('Upload admin')),
    (AVATAR_FROM_USERS, _('Upload user')),
)

class UsersAvatars(models.Model):
    title            = models.CharField(_('Avatar title'), max_length=255)
    owner            = models.ForeignKey(User, verbose_name=_('link to user'), blank=True, null=True)
    who_upload       = models.PositiveSmallIntegerField(_('who upload'), db_index=True, choices=WHO_UPLOADS, default=AVATAR_FROM_ADMIN)
    image_orig       = models.ImageField(_('Your avatar'), upload_to='upload/users/')
    
    class Meta:
        verbose_name = _(u'Users avatar')
        verbose_name_plural = _(u'Users avatars')
    
    def __unicode__(self):
        return u'%s' % self.title
            
    def delete(self):
        use_this_avatar = User.objects.filter(avatar=self)
        if use_this_avatar:
            for ava in use_this_avatar:
                ava.avatar = None
                ava.save()
        super(UsersAvatars, self).delete()

        
    ############################################################
    
class Friends(models.Model):
    requestor = models.ForeignKey(User, related_name='requestor')
    acceptor = models.ForeignKey(User, related_name='acceptor')
    accepted = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.datetime.today())
    
    def get_user(self):
        from apps.utils.middleware.threadlocals import get_current_user
        cur_user = get_current_user()
        if cur_user:
            if self.requestor==cur_user:
                return self.acceptor
            if self.acceptor==cur_user:
                return self.requestor
        return None
    user = property(get_user)
    
    def required_my_acception(self):
        from apps.utils.middleware.threadlocals import get_current_user
        cur_user = get_current_user()
        return not self.accepted and self.acceptor==cur_user
    
    class Meta:
        unique_together = (('requestor', 'acceptor'),)

MEN_SEX = 'm'
WOMAN_SEX = 'w'
SEX = (
    (MEN_SEX,_('men')),
    (WOMAN_SEX,_('women')),
)
    
# РАСШИРЕНИЕ МОДЕЛИ ПОЛЬЗОВАТЕЛЯ
User.add_to_class('avatar', models.ForeignKey(UsersAvatars, verbose_name=_('User standart avatar'), null=True, blank=True))
User.add_to_class('validation_code', models.PositiveIntegerField(verbose_name=_('Validation code'), default='123456'))

User.add_to_class('sex', models.CharField(verbose_name=_('sex'), max_length=1, choices = SEX, null=True, blank=True, default=None))
User.add_to_class('age', models.PositiveSmallIntegerField(verbose_name=_('age'), default=None, blank=True, null=True))
User.add_to_class('birthday', models.DateField(verbose_name=_('birthday'), default=None, blank=True, null=True))
User.add_to_class('metro', models.ForeignKey(Metro,verbose_name=_('user metro'), default=None, blank=True, null=True))
User.add_to_class('address', models.CharField(verbose_name=_('user_address'), max_length=255, null=True, blank=True, default=None))
#User.add_to_class('friends', models.ManyToManyField(User, verbose_name=_('Friends'), related_name='i_am_firend'))
#кол-во друзей
User.add_to_class('friends_num', models.PositiveIntegerField(verbose_name=_('Friends num'), default=0))
##кол-во друзей которые добавили меня
#User.add_to_class('friended_num', models.PositiveIntegerField(verbose_name=_('Friended num'), default=0))

# ФУНКЦИИ ЮЗЕРОВ
User.get_absolute_url = lambda (self): reverse('accounts_profile', kwargs={"username":self.username,})

User.get_avatar = lambda (self): render_to_string('accounts/get_avatar.html', {'self': self})

def add_friend(self, friend):
    if not self.in_friends(friend):
        fr, cr = Friends.objects.get_or_create(requestor=self, acceptor=friend)
        if cr:
            self.friends_num+=1
            self.save()
            friend.friends_num+=1
            friend.save()
            return True
    return False

def delete_friend(self, friend):
    if self.in_friends(friend):
        fr = Friends.objects.filter(models.Q(requestor=self, acceptor=friend)|models.Q(acceptor=self, requestor=friend))
        if self.friends_num>0:
            self.friends_num-=1
            self.save()
        if friend.friends_num>0:
            friend.friends_num-=1
            friend.save()
        fr.delete()
        return True
    return False
        
def accept_friend(self, friend):
    fr = Friends.objects.get(acceptor=self, requestor=friend)
    if not fr.accepted:
        fr.accepted = True
        fr.save()
        return True
    return False

    
def actual_friends(self):
    return User.objects.distinct().filter(
                               models.Q(acceptor__requestor=self, acceptor__accepted=True)|
                               models.Q(requestor__acceptor=self, requestor__accepted=True)
                               )


#def get_friends(self):
#    res = Friends.objects.filter(models.Q(acceptor=self)|models.Q(requestor=self)).order_by('-date').all()[:]
#    return [{'user':li.requestor, 'date':li.date, 'accepted':li.accepted} for li in res if li.acceptor == self and not li.accepted] + \
#           [{'user':li.requestor, 'date':li.date, 'accepted':li.accepted} for li in res if li.acceptor == self and li.accepted] + \
#           [{'user':li.acceptor, 'date':li.date, 'accepted':True} for li in res if li.requestor == self]
def all_friends(self):
    return Friends.objects.filter(models.Q(acceptor=self)|models.Q(requestor=self)).order_by('-date')

def get_new_friends(self):
    return Friends.objects.filter(acceptor=self, accepted=False).order_by('-date')

def in_friends(self, friend):
    return bool(Friends.objects.filter(
                                       models.Q(requestor=self, acceptor=friend) |
                                       models.Q(acceptor=self, requestor=friend)
                                       ).count()
                )
    

User.actual_friends = actual_friends
User.in_friends = in_friends
User.add_friend = add_friend
User.delete_friend = delete_friend
User.all_friends = all_friends
User.get_new_friends = get_new_friends
User.accept_friend = accept_friend
User.get_full_name = lambda (self) : u'%s %s' % (self.last_name, self.first_name) if self.first_name!='' and self.last_name!='' else self.username


def rating_percent(self):
    p=RangHistory.objects.filter(event__author=self).aggregate(Avg('rang'))
    rang = p['rang__avg'] if p['rang__avg'] else 0
    return  int(rang/5*100)

User.rating_percent = rating_percent