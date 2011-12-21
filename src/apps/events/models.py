# coding: utf-8
from django.utils.translation       import ugettext_lazy as _

from django.db                      import models
from django.contrib.auth.models import User
from datetime import datetime, date, time
from django.template.loader import render_to_string
from django.db.models import Avg
from django.contrib.contenttypes import generic
from apps.video_convertor.models import Video
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
#from django.core.urlresolvers import reverse


__all__ = ('City', 'Metro', 'CategoryGroup', 'Category', 'Event', 'Meeting',
           'RangHistory', 'User', 'Ban',
           'Photo', 'CachedSearch','EventInvite', 'AssistantRequest')



#Город
class City(models.Model):
    #название
    name = models.CharField(max_length=255, verbose_name=_(u'название'))

    __unicode__ = lambda self: u"%s" % self.name

    class Meta():
        verbose_name=_(u'Город')
        verbose_name_plural=_(u'Город')
        ordering = ('name', )

#Район
class Metro(models.Model):
    #название
    name = models.CharField(max_length=255, verbose_name=_(u'название'))
    #город
    city = models.ForeignKey(to='City', verbose_name=_(u'город'), related_name='region_city_city_set')

    __unicode__ = lambda self: u"%s" % self.name

    class Meta():
        verbose_name=_(u'Метро')
        verbose_name_plural=_(u'Метро')
        ordering = ('name', )

#Группа категорий
class CategoryGroup(models.Model):
    #название
    name = models.CharField(max_length=255, verbose_name=_(u'название'))
    
    __unicode__ = lambda self: u"%s" % self.name


    class Meta():
        verbose_name=_(u'Группа категорий')
        verbose_name_plural=_(u'Группа категорий')
        ordering = ('name', )

#Категория
class Category(models.Model):
    #название
    name = models.CharField(max_length=255, verbose_name=_(u'название'))
    #группа
    group = models.ForeignKey(to='CategoryGroup', verbose_name=_(u'группа'), related_name='category_group_categorygroup_set')
    __unicode__ = lambda self: u"%s" % self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ("events_list", [], {'category': self.id})

    class Meta():
        verbose_name=_(u'Категория')
        verbose_name_plural=_(u'Категория')
        ordering = ('name', )
        
        
##стадии жизни события
#STATE_IDEA = 1          # идея проведения события (переходит по рейтингу - верхние в топе идей)
#STATE_ORGANIZATION = 2  # организация события - (переход в следующую - если корректны
#                        # все данные, время в будущем, координатор и модератор одобрели событие)
#STATE_COMPLITE = 3      # событие будет вроведено или уже проведено (зависит от даты и текущего временя)
#    
#STATE = (
#    (STATE_IDEA, _('STATE_IDEA')),
#    (STATE_ORGANIZATION, _('STATE_ORGANIZATION')),
#    (STATE_COMPLITE, _('STATE_COMPLITE')),
#)


#Событие
class Event(models.Model):

    #краткое название
    title = models.CharField(max_length=255, verbose_name=_(u'название'))

    #Метатэги
    seo_title       = models.CharField(_('title for SEO'), max_length=255, blank=True)
    seo_keywords    = models.CharField(_('keywords for SEO'), max_length=255, blank=True)
    seo_description = models.CharField(_('description for SEO'), max_length=255, blank=True)

#    state = models.PositiveSmallIntegerField(verbose_name=_('event state'), choices =  STATE, default = STATE_IDEA, db_index=True)
    is_idea = models.BooleanField(verbose_name=_('is idea'), editable=False, default=True)
    idea_rang = models.IntegerField(verbose_name=_('idea rang'), default=0)
    #полное описание
    description = models.TextField(verbose_name=_(u'описание'), blank=True)
#    address = models.CharField(verbose_name=_(u'адрес'), max_length=255, blank=True)
#    place = models.CharField(verbose_name=_(u'место'), max_length=255, blank=True)
#    #начало
#    begin = models.DateTimeField(verbose_name=_(u'начало'))
#    #конец
#    end = models.DateTimeField(verbose_name=_(u'конец'))
#    #район
#    metro = models.ForeignKey(Metro, verbose_name=_(u'метро'))
    #координатор
    author = models.ForeignKey(User, verbose_name=_(u'Автор идеи'), related_name='events_author') #, editable = False
#    #опубликовано координатором
#    published_by_author = models.BooleanField(verbose_name=_(u'опубликовано координатором'))
#    #опубликовано модератором
#    published_by_moderator = models.BooleanField(verbose_name=_(u'опубликовано модератором'))
    is_interzet = models.BooleanField(verbose_name=_(u'отмечено InterZet'))
    #категория
    category = models.ForeignKey(to='Category', verbose_name=_(u'категория'), related_name='event_category_category_set')
#    #событие недели
#    event_of_week = models.BooleanField(verbose_name=_(u'событие недели'))
    
    photo = models.ImageField(upload_to='upload/', verbose_name=_(u'обложка'), blank=True, null=True)
        
    cached_rang = models.PositiveIntegerField(editable = False, default=0)
    cached_ball = models.PositiveSmallIntegerField(editable = False, default=0,verbose_name=_(u'заполненность'))
    
    assistents = models.ManyToManyField(User, related_name="assistent_for_events")

    date_create = models.DateField(u'Дата создания', auto_now_add=True,null=True,blank=True)

    accept_moder = models.BooleanField(u'Разрешено модератором', default=True )
    

    __unicode__ = lambda self: self.title

    
    class Meta():
        verbose_name=_(u'Событие')
        verbose_name_plural=_(u'Событие')
        ordering = ('title', )
    
    def save(self):
        self.cached_ball = self.get_start_ball()
        if not self.id:
            self.is_idea=True
        else:
            self.is_idea =  self.meetings.count() == 0

            
        super(Event, self).save()
        
    def soon_next_meeting(self):
        try:        
            return self.meetings.filter(end__gt=datetime.today(),accept_moder=True).order_by('end')[0]
        except:
            pass
        return None
    
    def soon_prev_meeting(self):
        try:        
            return self.meetings.filter(end__lt=datetime.today(),accept_moder=True).order_by('-end')[0]
        except:
            pass
        return None
    
    def soon_meeting(self):
        if not hasattr(self, '_soon_meeting'):
            self._soon_meeting = self.soon_next_meeting()
            if not self._soon_meeting:
                self._soon_meeting = self.soon_prev_meeting()
        return self._soon_meeting
    
#    def get_state_display(self):
#        if self.is_idea:
#            return u"идея"
#        meeting = self.soon_next_meeting()
#        if meeting and meeting.end>datetime.today():
#            return "сформированное"
#        return "прошедшее"
        
        
#    def make_complite_to_organization(self):
#        self.state = STATE_ORGANIZATION
#        self.published_by_author = False
#        self.published_by_moderator = False
#        self.save()
#    
#    def make_idea_to_organization(self):
#        self.state = STATE_ORGANIZATION
#        self.save()
#        self.make_organization_to_complite()
#        return True
#        
#    def test_for_complite(self):
#        return  (self.state == STATE_ORGANIZATION and self.published_by_author and self.published_by_moderator)
#    
#    def make_organization_to_complite(self):
#        if self.test_for_complite():
#            self.state = STATE_COMPLITE
#            self.save()
#            return True
#        return False
#        
#    def is_idea_state(self):
#        return self.state == STATE_IDEA
#
#    def is_organization_state(self):
#        return self.state == STATE_ORGANIZATION
#    
#    def is_complite_state(self):
#        return self.state == STATE_COMPLITE
        
    def random_visiters(self):
        return self.visiters.order_by('?')[:10]
    
    def actual_comments(self):
        return self.comment_set.filter(state=self.state).order_by('-created')

    def last_comments(self):
        return self.actual_comments()[:10]
    

            
    def rating_percent(self):
#        p=RangHistory.objects.filter(event=self).aggregate(Avg('rang'))
#        rang = p['rang__avg'] if p['rang__avg'] else 0
        return  int(self.cached_rang/50)
    
    def get_photo(self):
        if self.photo:
            return self.photo
        if self.author.avatar:
            return self.author.avatar.image_orig
        return None
    
    def my_friends_visiters_count(self):
        if not hasattr(self, '_my_friends_visiters_count'):
            from apps.utils.middleware.threadlocals import get_current_user
            user = get_current_user()
            if user:
                self._my_friends_visiters_count =  user.actual_friends().filter(events_visit=self).count()
            else:
                self._my_friends_visiters_count = "???"
        return self._my_friends_visiters_count
    
    def can_i_set_rating(self):
        from apps.utils.middleware.threadlocals import get_current_user
        user = get_current_user()
        if user.is_authenticated():
            qs = IdeaRangHistory.objects.filter(event=self, user = user)
            return qs.count()==0
        return False    

 
#        return (user in self.visiters.all() or user==self.author) and self.end<datetime.today()
#        return qs.count()==0

    def can_add_photo(self, user):
        return True
#        return self.author==user or ( user in self.visiters.all() and self.end<datetime.today() \
#                                      and self.state==STATE_COMPLITE)
    
    def can_i_add_photo(self):
        from apps.utils.middleware.threadlocals import get_current_user
        return self.can_add_photo(get_current_user())

    
    def all_photo(self):
        return self.photo_set.exclude(models.Q(photo=None) | models.Q(photo="")).order_by('created')


    def can_add_video(self, user):
        return True
    
    def can_i_add_video(self):
        from apps.utils.middleware.threadlocals import get_current_user
        return self.can_add_photo(get_current_user())
    
    def all_video(self):                        
        return Video.objects.related_and_processed(self)

    def get_video_add_url(self):
        ct=ContentType.objects.get_for_model(self)
        return reverse("video_upload", args=(ct.id, self.id)) 

#    def can_i_make_organization(self):
#        from apps.utils.middleware.threadlocals import get_current_user
#        user = get_current_user()
#        return self.author==user and self.end<datetime.today() \
#                                      and self.state==STATE_COMPLITE\
#                                      and self.cached_rang>=4000
        
    
    def rating(self, user, rang):
        qs = RangHistory.objects.filter(event=self, user = user)
        if qs.count()==0:    
            RangHistory(event=self, user = user, rang = rang).save()
            rang = RangHistory.objects.filter(event=self).aggregate(models.Avg('rang'))['rang__avg']
            self.cached_rang=rang*1000 if rang else 0
            self.save()
            return True
        return False
    
    def idea_rating(self, user, rang):
        qs = IdeaRangHistory.objects.filter(event=self, user = user)
        if qs.count()==0:    
            IdeaRangHistory(event=self, user = user, rang = rang).save()
            self.idea_rang+=rang
            self.save()
            return True
        return False

    
    @models.permalink
    def get_absolute_url(self):
        return ('events_one', [self.id])

    @models.permalink
    def get_absolute_url_moderator(self):
        return ('events_moderation_id', [self.id])

    def get_start_ball(self):
        ball=0
        if self.title:
            ball+=10
        if self.category:
            if self.category.name.find(u"разно")==-1:                
                ball+=20
            else:
                ball+=10
        
        if self.description:
            if len(self.description.split(" "))>3:
                ball+=10
        if self.photo:
            ball+=15
            
        meeting = self.soon_meeting()
        if meeting:
            ball+=20
        
        return ball
    

class MeetingManager(models.Manager):
    
    def actual(self):
        return self.filter(end__gte=datetime.today())
    
    def for_top(self):
        return self.filter(end__lt=datetime.today())

        
class Meeting(models.Model):
    objects = MeetingManager()
    
    author = models.ForeignKey(User, related_name='meetings')
    
    event = models.ForeignKey(Event, related_name='meetings')
#    description = models.TextField(verbose_name=_(u'описание'), blank=True)
    address = models.CharField(verbose_name=_(u'адрес'), max_length=255, blank=True)
    place = models.CharField(verbose_name=_(u'место'), max_length=255, blank=True)
    #начало
    begin = models.DateTimeField(verbose_name=_(u'начало'))
    #конец
    end = models.DateTimeField(verbose_name=_(u'конец'),null=True,blank=True)
    #район
    metro = models.ForeignKey(Metro, verbose_name=_(u'метро'))
    #мин. ограничение участников
    min_participants = models.PositiveIntegerField(null=True, verbose_name=_(u'мин. ограничение участников'), blank=True)
    #макс. ограничение участников
    max_participants = models.PositiveIntegerField(null=True, verbose_name=_(u'макс. ограничение участников'), blank=True)
    #пойдут на мероприятие
    visiters = models.ManyToManyField(User, null=True, verbose_name=_(u'пойдут на мероприятие'), blank=True, editable=False, related_name="events_visit")
    
    cached_ball = models.PositiveSmallIntegerField(editable = False, default=0,verbose_name=_(u'заполненность'))
    
    accept_moder = models.BooleanField(u'Разрешено модератором', default=True )


    __unicode__ = lambda self: u"%s [%s..%s]" % (self.event.title, self.begin, self.end)
    
    class Meta():
        verbose_name=_(u'Встреча')
        verbose_name_plural=_(u'Встречи')
        ordering = ('begin','-cached_ball', )
    
    @models.permalink
    def get_absolute_url(self):
        return ('events_one_meeting', [self.event.id, self.id])
    @models.permalink
    def get_absolute_url_moderator(self):
        return ('events_moderation_id_meeting', [self.event.id, self.id])
        
    def save(self):
        is_new = not self.id
        self.cached_ball = self.get_start_ball()
        super(Meeting, self).save()        
        if is_new:
            if self.event.is_idea:
                self.event.is_idea=False
                self.event.save()              
            #Automatic add author in visiters in new Metting
            self.visiters.add(self.event.author)
                
    def is_equal_date(self):
        return date(self.begin.year, self.begin.month, self.begin.day)==\
            date(self.end.year, self.end.month, self.end.day)

    def is_equal_time(self):
        return time(self.begin.hour, self.begin.min)==\
            time(self.end.hour, self.end.min)
    
    def can_i_invite(self):
        from apps.utils.middleware.threadlocals import get_current_user
        user = get_current_user()
        return user.is_authenticated() and self.end>datetime.today()

    def can_i_visit(self):
        from apps.utils.middleware.threadlocals import get_current_user
        user = get_current_user()
        return user.is_authenticated() and self.end>datetime.today()
    
    def i_am_visiters(self):
        from apps.utils.middleware.threadlocals import get_current_user
        return bool(get_current_user() in self.visiters.all())
    
    def is_past(self):
        return self.end<datetime.today()
    
    def get_start_ball(self):
        ball= self.event.get_start_ball()
        if self.address:
            ball+=10
        if self.place:
            ball+=10
        if self.min_participants and self.max_participants:
            ball+=5
        
        return ball

    def limited_visiters_list(self):
        return self.visiters.all()[:30]

    def visiters_more_then_limit(self):
        return self.visiters_count()>30
    
    def visiters_count(self):
        if not hasattr(self, "_visiters_count"):
            self._visiters_count = self.visiters.count()
        
        return self._visiters_count


#Рейтинг - история
class IdeaRangHistory(models.Model):
    #собтие
    event = models.ForeignKey(to='Event', verbose_name=_(u'собтие'))
    #кто
    user = models.ForeignKey(User, verbose_name=_(u'кто'))
    #оценка
    rang = models.SmallIntegerField(verbose_name=_(u'оценка'), default=0)
    #когда
    datetime = models.DateTimeField(verbose_name=_(u'когда'), auto_now_add = True)

    class Meta():
        unique_together = (('event', 'user'),)
        
#Рейтинг - история
class RangHistory(models.Model):
    #собтие
    event = models.ForeignKey(to='Event', verbose_name=_(u'собтие'))
    #кто
    user = models.ForeignKey(User, verbose_name=_(u'кто'))
    #оценка
    rang = models.IntegerField(verbose_name=_(u'оценка'))
    #когда
    datetime = models.DateTimeField(verbose_name=_(u'когда'), auto_now_add = True)

    class Meta():
        verbose_name=_(u'Рейтинг - история')
        verbose_name_plural=_(u'Рейтинг - история')
        unique_together = (('event', 'user'),)

#Черные метки
class Ban(models.Model):
    #кого
    user = models.ForeignKey(User, verbose_name=_(u'кого'), related_name='ban_user_user_set')
    #событие
    event = models.ForeignKey(to='Event', verbose_name=_(u'событие'), related_name='ban_event_event_set')
    #когда
    when = models.DateTimeField(verbose_name=_(u'когда'))
    #кто отметил
    who = models.ForeignKey(User, verbose_name=_(u'кто отметил'), related_name='ban_who_user_set')
    #причина
    reason = models.TextField(verbose_name=_(u'причина'), blank=True)

    __unicode__ = lambda self: u"%s" % self.reason

    class Meta():
        verbose_name=_(u'Черные метки')
        verbose_name_plural=_(u'Черные метки')

#Фото
class Photo(models.Model):
    #событие
    event = models.ForeignKey(to='Event', verbose_name=_(u'событие'), related_name="photo_set")
    #когда
    created = models.DateTimeField(verbose_name=_(u'когда'), auto_now_add = True)
    #фотография
    photo = models.ImageField(upload_to='upload/', verbose_name=_(u'фотография'), blank=True)
    #подпись
    title = models.CharField(max_length=255, verbose_name=_(u'подпись'), blank=True)
    #опубликовано координатором
    published = models.BooleanField(verbose_name=_(u'опубликовано автором идеи'))
    #кто
    author = models.ForeignKey(User, verbose_name=_(u'кто'), related_name='photo_author_set')
    
    @models.permalink
    def get_absolute_url(self):
        return ("events_photo", (self.id,))

    class Meta():
        verbose_name=_(u'Фото')
        verbose_name_plural=_(u'Фото')
        
    def delete(self):
        super(Photo, self).save()
        if self.photo:
            self.photo.delete()
        

##Видео
#class Video(models.Model):
#    #событие
#    event = models.ForeignKey(to='Event', verbose_name=_(u'событие'), related_name='video_event_event_set')
#    #когда
#    created = models.DateTimeField(verbose_name=_(u'когда'))
#    #видео
#    video = models.FileField(upload_to='upload/', verbose_name=_(u'видео'), blank=True)
#    #подпись
#    title = models.CharField(max_length=255, verbose_name=_(u'подпись'), blank=True)
#    #опубликовано координатором
#    published = models.BooleanField(verbose_name=_(u'опубликовано координатором'))
#    #кто
#    user = models.ForeignKey(User, verbose_name=_(u'кто'), related_name='video_user_user_set')
#
#    class Meta():
#        verbose_name=_(u'Видео')
#        verbose_name_plural=_(u'Видео')

##Комментарий
#class Comment(models.Model):
#    #событие
#    event = models.ForeignKey(to='Event', verbose_name=_(u'событие'))
#    #кто
#    user = models.ForeignKey(User, verbose_name=_(u'кто'))
#    #когда
#    created = models.DateTimeField(verbose_name=_(u'когда'), auto_now_add = True)
#    #сообщение
#    text = models.TextField(verbose_name=_(u'сообщение'))
#    
#    state = models.PositiveSmallIntegerField(verbose_name=_('comment state'), choices =  STATE, default = STATE_IDEA, db_index=True)
#
#    __unicode__ = lambda self: u"%s" % self.text
#
#    class Meta():
#        verbose_name=_(u'Комментарий')
#        verbose_name_plural=_(u'Комментарий')
#        ordering = ('-created', )
        
        
class EventInvite(models.Model):
    event = models.ForeignKey(Event)
    meeting = models.ForeignKey(Meeting)
    user = models.ForeignKey(User, related_name='event_invite')
    who = models.ForeignKey(User, related_name='my_event_invite')
    when = models.DateTimeField(auto_now_add = True)
    accepted = models.NullBooleanField(default=None)
    deleted = models.BooleanField(default=False)
    
    is_accepted = lambda self: self.accepted==True
    is_rejected = lambda self: self.accepted==False
    is_new = lambda self: self.accepted==None
    
    class Meta():
        unique_together = (('event', 'user',),)
        ordering = ('-when', )
        
#class FilterManager(models.Manager):
#    
#        
#    def by_key(self, key):
#        try:
#            return self.get(key = key)
#        except:
#            return None
                    

class CachedSearch(models.Model):
#    objects = FilterManager()
    
#    key = models.CharField(max_length=32, editable = False, db_index = True, unique = True)
    string = models.CharField(verbose_name=_(u'Запрос'), db_index = True, max_length=255, blank=True, null=True)
#    date = models.DateField(verbose_name=_(u'Дата'), blank=True, null=True)
#    city = models.ForeignKey(City,verbose_name=_(u'Город'), blank=True, null=True)
#    category = models.ManyToManyField(Category, verbose_name=_(u'Категория'), blank=True, null=True)


#    def create_key(self, data):
#        import md5
#        key_val ="%s_%s_%s_%s" % (data['string'],
#                                  data['date'],
#                                  data['city'],
#                                  "_".join(map(lambda e: "%s" % e.id, data['category']))
#                                  )
#        print "** key val", key_val
#        return md5.new(key_val).hexdigest()
#    
#    def filter(self, events):
#        if self.date:
#            events = events.filter(begin__lte = self.date, end__gte = self.date)
#        if self.city:
#            events = events.filter(metro__city = self.city)
#        category = self.category.all()
#        if category:
#            events = events.filter(category__in = category)
#        return events
    


#    def make_key(self, data):
#        self.key = self.create_key(data)

        
#    def save(self):
#        super(Filter, self).save()


class AssistantRequest(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    
    class Meta():
        unique_together = (('user', 'event',),)
