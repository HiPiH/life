# coding: utf-8
from apps.accounts.models import *
from apps.events.models import *
from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from pytils import numeral
from apps.utils.forms import SelectGraphDate
import base64
import cPickle
import datetime, time
import urllib
from django.utils.encoding import force_unicode

###!!!!!
import form_patch


__all__ = ('FilterForm', 'CreateEventForm','EditIdeaEventForm','EditAcceptedEventForm',
           'InviteForm','FriendsFilterForm', 'MeetingForm', 'IdeaFilterForm',)


class FilterForm(forms.Form):
    string = forms.CharField(label=_(u'Название'), required = False)
    date = forms.DateField(widget=SelectGraphDate({'showsTime':"false",}), required = False)
    date2 = forms.DateField(widget=SelectGraphDate({'showsTime':"false",}), required = False)
    metro = forms.ModelChoiceField(Metro.objects.all(), empty_label=u"все", required = False)
    category = forms.ModelMultipleChoiceField(
                                        Category.objects.all(),
                                        widget = forms.CheckboxSelectMultiple,
                                        required = False
                                      )
    is_archive = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kwargs):
        if 'initial' in kwargs:
            if 'string' in kwargs['initial']:
                id = kwargs['initial']['string']
                try:
                    cached_search = CachedSearch.objects.get(pk = id)
                    kwargs['initial']['string'] = cached_search.string
                except:
                    kwargs['initial']['string'] = ''
                    
            if kwargs['initial']['category']:
                kwargs['initial']['category'] = kwargs['initial']['category'].split('-')
               
            kwargs['initial']['is_archive']=kwargs['initial']['is_archive']=='1'
                
                
        super(FilterForm, self).__init__(*args, **kwargs)
    
    def make_url(self):
        arg={}
            
        kwargs={}
        
        if 'string' in self.cleaned_data and self.cleaned_data['string']:
            cached_search, created  = CachedSearch.objects.get_or_create(string = self.cleaned_data['string'])
            kwargs['string'] = cached_search.id
            
        if self.cleaned_data['date']:
            kwargs['date'] = self.cleaned_data['date']

        if self.cleaned_data['date2']:
            kwargs['date2'] = self.cleaned_data['date2']
        
#        if self.cleaned_data['city']:
#            kwargs['city'] = self.cleaned_data['city'].id

        if self.cleaned_data['metro']:
            kwargs['metro'] = self.cleaned_data['metro'].id

        if self.cleaned_data['category']:
            kwargs['category'] = "-".join(map(lambda e: "%s" % e.id, self.cleaned_data['category']))
            
        if self.cleaned_data['is_archive']:
            kwargs['is_archive'] = 1 if self.cleaned_data['is_archive'] else 0

#
        return reverse("events_list", kwargs=kwargs)
    
    def filter(self, meetings):
        
        if self.is_valid():
            data = self.cleaned_data
        else:
            data = self.initial
            
            
        if 'string' in data and data['string']:
            meetings = meetings.filter(event__title__icontains = data['string'])
            
        if 'date' in data and  data['date']:
            date = datetime.date(*time.strptime(data['date'], "%Y-%m-%d")[:3])
            lo_date = date
            hi_date = date + datetime.timedelta(1)
            meetings = meetings.filter(end__gte = lo_date)
        
        if 'date2' in data and  data['date2']:
            date2 = datetime.date(*time.strptime(data['date2'], "%Y-%m-%d")[:3])
            lo_date2 = date2
            hi_date2 = date2 + datetime.timedelta(1)
            meetings = meetings.filter(begin__lt = hi_date)

        if 'metro' in data and  data['metro']:
            meetings = meetings.filter(metro__id = data['metro'])
#        if data['city']:
#            events = events.filter(metro__city__id = data['city'])
        if 'category' in data and  data['category']:
            meetings = meetings.filter(event__category__in = data['category'])
            
            
        if 'is_archive' in data and data['is_archive']:
            meetings = meetings.filter(end__lt=datetime.datetime.today())
        else:
            #meetings in next time
            meetings = meetings.filter(end__gte=datetime.datetime.today())
        return meetings
    
class IdeaFilterForm(forms.Form):
    string = forms.CharField(label=_(u'Название'), required = False)
    category = forms.ModelMultipleChoiceField(
                                        Category.objects.all(),
                                        widget = forms.CheckboxSelectMultiple,
                                        required = False
                                      )
    def __init__(self, *args, **kwargs):
        if 'initial' in kwargs:
            if 'string' in kwargs['initial']:
                id = kwargs['initial']['string']
                try:
                    cached_search = CachedSearch.objects.get(pk = id)
                    kwargs['initial']['string'] = cached_search.string
                except:
                    kwargs['initial']['string'] = ''
                    
            if  'category' in kwargs['initial'] and kwargs['initial']['category']:
                kwargs['initial']['category'] = kwargs['initial']['category'].split('-')
               
        super(IdeaFilterForm, self).__init__(*args, **kwargs)
    
    def make_url(self):
        arg={}
        kwargs={}
        if 'string' in self.cleaned_data and self.cleaned_data['string']:
            cached_search, created  = CachedSearch.objects.get_or_create(string = self.cleaned_data['string'])
            kwargs['string'] = cached_search.id
            
        if self.cleaned_data['category']:
            kwargs['category'] = "-".join(map(lambda e: "%s" % e.id, self.cleaned_data['category']))
            
        return reverse("events_idea_filter", kwargs=kwargs)
    
    def filter(self, events):
        
        if self.is_valid():
            data = self.cleaned_data
        else:
            data = self.initial
            
        if 'string' in data and data['string']:
            events = events.filter(title__icontains = data['string'])
        if 'category' in data and  data['category']:
            events = events.filter(category__in = data['category'])
        return events


class CreateEventForm(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = ['title',
                  'category',  
                  'description',
                  'photo',
                  ]
        
class MeetingForm(forms.ModelForm):
    
    begin = forms.DateTimeField(label=_(u'Начало'), widget=SelectGraphDate({'showsTime':"true", 'ifFormat':     "\"%Y-%m-%d %H:%M\"",}))
    end = forms.DateTimeField(label=_(u'Конец'), widget=SelectGraphDate({'showsTime':"true", 'ifFormat':     "\"%Y-%m-%d %H:%M\"",}))

    class Meta:
        model = Meeting
        fields = [
                   'begin','end', 
                  'metro',
                  'address','place', 
                  'min_participants','max_participants',                  
                  ]
        

class EditIdeaEventForm(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = ['title',
                  'category', 
                   'description',
                  'photo'
                  ]
        
class EditAcceptedEventForm(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = ['category', 'description', 'photo',]
        
UNKNOWN_SEX = ''
SEX_CHOICE=(
    (UNKNOWN_SEX, _('unknown sex')),
    (MEN_SEX,_('men')),
    (WOMAN_SEX,_('women')),
)

class InviteForm(forms.Form):
    min_age = forms.IntegerField(label=_('min_age'), required=False, min_value=5, max_value=90)
    max_age = forms.IntegerField(label=_('max_age'), required=False, min_value=5, max_value=90)
    sex = forms.CharField(label=_('sex'), required=False,
                          widget=forms.Select(choices=SEX_CHOICE))
    city_connect = forms.BooleanField(label=_('connect users to event city'), required=False)
    metro_connect = forms.BooleanField(label=_('connect users to event metro'), required=False)
    users = forms.ModelMultipleChoiceField(required=False,
                                           label=_('user list'),
                                           queryset = User.objects.all(),
                                           widget=forms.CheckboxSelectMultiple)
    
    def __init__(self, cur_user, cur_event, *args,**kwargs):
        super(InviteForm, self).__init__(*args, **kwargs)
        self.cur_user = cur_user
        self.cur_event = cur_event
#        dir(self)

        users = cur_user.actual_friends()
        #remove already invited or visited users
        invited_or_visiters_ids = User.objects.distinct().filter(
                                    models.Q( event_invite__event=self.cur_event )|
                                    models.Q( events_visit=self.cur_event )
                                    ).values_list('id')
        if invited_or_visiters_ids:
            invited_or_visiters_ids = map(lambda e: e[0], invited_or_visiters_ids)
            users=users.exclude(id__in=invited_or_visiters_ids)

        self.fields['users'].queryset = users
        
    def clean(self):
        users = self.cur_user.actual_friends()
        
        if self.cleaned_data['min_age']:
            min_birthday = datetime.date.today() - datetime.timedelta(365 * self.cleaned_data['min_age'])
            users = users.filter(birthday__lte=min_birthday)
            

        if self.cleaned_data['max_age']:
            max_birthday = datetime.date.today() - datetime.timedelta(365 * self.cleaned_data['max_age'])
            users = users.filter(birthday__gte=max_birthday)
            
        if 'sex' in  self.cleaned_data and self.cleaned_data['sex']:
            users = users.filter(sex = self.cleaned_data['sex'])
        
        if self.cleaned_data['metro_connect']:
            users = users.filter(metro = self.cur_event.metro)
        elif self.cleaned_data['city_connect']:
            users = users.filter(metro__city = self.cur_event.metro.city)
            
        self.fields['users'].queryset = users
        return self.cleaned_data

    
def age_choices():
    return [('','---')]+[(age,age) for age in xrange(10,80)]
    
class FriendsFilterForm(forms.Form):
    string = forms.CharField(label=_(u'Название'), required = False)
    age = forms.IntegerField(label=_(u'Age'), required=False,
                             widget=forms.Select(choices=age_choices())
                             )
    address = forms.CharField(label=_(u'Адрес'), required = False)
    
#    def __init__(self, *args, **kwargs):
#        if 'initial' in kwargs:
#            if 'string' in kwargs['initial'] and kwargs['initial']['string']:
#                s = kwargs['initial']['string']
#                print s, type(s)
##                print urllib.unquote(s)
#                kwargs['initial']['string'] = s
#
#            if 'address' in kwargs['initial'] and kwargs['initial']['address']:
#                s = kwargs['initial']['address']
#                kwargs['initial']['address'] = s
#                
#        super(FriendsFilterForm, self).__init__(*args, **kwargs)
#    
    def make_url(self):
#        urllib.unquote
        arg={}
            
        kwargs={}
        
        if 'string' in self.cleaned_data and self.cleaned_data['string']:
            s=self.cleaned_data['string']
            kwargs['string'] = urllib.quote(s.encode("utf-8")) 
            
        if self.cleaned_data['age']:
            kwargs['age'] = self.cleaned_data['age']

        if 'address' in self.cleaned_data and self.cleaned_data['address']:
            s=self.cleaned_data['address']
            kwargs['address'] = urllib.quote(s.encode("utf-8"))

#
        return reverse("events_friends", kwargs=kwargs)
#    
    def filter(self, users):
        
        if self.is_valid():
            data = self.cleaned_data
        else:
            data = self.initial
            
        if data['string']:
            users = users.filter(
                                   models.Q(username__icontains = data['string'])
                                 | models.Q(first_name__icontains = data['string'])
                                 | models.Q(last_name__icontains = data['string'])
                                 )
        if data['address']:
            users = users.filter(models.Q(address__icontains = data['address']))
            
        if data['age']:
            lo_birthday = datetime.date.today() - datetime.timedelta(365 * (int(data['age'])+1))
            hi_birthday = datetime.date.today() - datetime.timedelta(365 * int(data['age']))
            users = users.filter(birthday__gte = lo_birthday, birthday__lte = hi_birthday)
        return users
    
#class CommentForm(forms.ModelForm):
#    
#    class Meta:
#        model = Comment
#        fields = ['text']
 