# coding: utf-8
from apps.events.config import config
from apps.events.forms import *
from apps.events.models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound,\
    Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _, ugettext
from django.db import models
from lib.shortcuts import render_to, ajax_request
import datetime
from apps.video_convertor.forms import VideoForm


@render_to('events/index.html')
def index(req):
    out={}
    out['filter'] =  FilterForm()
    out['meetings'] = Meeting.objects.actual()
    return out


@render_to('events/list.html')
def list(req, page_num=None, target=None, big_url=False, **kwargs):
    
    out={}

    out['big_url']=big_url
    out['target']=target
    if 'date' in kwargs:
        req.events_filter_date = kwargs['date']
    if 'date2' in kwargs:
        req.events_filter_date2 = kwargs['date2']
    if req.POST:
        out['filter'] = form = FilterForm(req.POST)
        if form.is_valid():
            return HttpResponseRedirect(form.make_url())
    else:
        out['filter'] = form =  FilterForm(initial = kwargs)
        
    meetings = Meeting.objects.filter(Q(accept_moder=True))
    if req.user.is_authenticated():
        if target=="my":            
            meetings=Meeting.objects.filter( models.Q(event__author=req.user) |  models.Q(author = req.user))
        if target=="where_im_going":
            meetings=meetings.filter(visiters=req.user)
        if target=="friends":
            meetings=meetings.filter(
                                 models.Q(event__author__requestor__acceptor=req.user, event__author__requestor__accepted=True)|
                                 models.Q(event__author__acceptor__requestor=req.user, event__author__acceptor__accepted=True)
                                 )
        if target=="friends_going":
            meetings=meetings.filter(
                                 models.Q(visiters__requestor__acceptor=req.user, visiters__requestor__accepted=True)|
                                 models.Q(visiters__acceptor__requestor=req.user, visiters__acceptor__accepted=True)
                                 )

    meetings = form.filter(meetings)
    
    out['meetings'] = meetings

    pagin=Paginator(meetings, config.events_per_page())
    out['paginator']=pagin
    out['page']=page=pagin.page(int(page_num) if page_num else 1)

    out['is_archive'] = kwargs['is_archive']

    
    return out

#@render_to('events/list_organization.html')
#def list_organization(req, page_num=None):
#    out={}
#    out['events'] = Event.objects.filter(state = STATE_ORGANIZATION)
#
#    pagin=Paginator(events, config.events_per_page())
#    out['paginator']=pagin
#    out['page']=page=pagin.page(int(page_num) if page_num else 1)
#    
#    return out

@render_to('events/one.html')
def one(req, id, meeting_id = None):
    out={}    
    out['event'] = event = get_object_or_404(Event,Q(accept_moder=True)|Q(author=req.user), pk = id)
    
    if meeting_id:
        out['meeting'] = meeting = get_object_or_404(Meeting,Q(accept_moder=True)|Q(author=req.user), pk=meeting_id, event = event)
        out['i_am_visitor'] = meeting.visiters.all().filter(id=req.user.id).count()
    else:
        meeting = event.soon_meeting()
        if meeting:
            return HttpResponseRedirect(meeting.get_absolute_url())
        
    if meeting:
        out['i_am_visiters'] = req.user in meeting.visiters.all()
        if req.user.is_authenticated():
            out['my_frend_visiters_visiters'] = meeting.visiters.all().filter(id__in=req.user.actual_friends().values('id')).count()
        

    
    #out['assistant_requests_count'] = AssistantRequest.objects.filter(user = req.user, event=event).count()
    
    out['i_am_author'] = (req.user == event.author) or (req.user in event.assistents.all())
    if req.user.is_authenticated():
        out['invite_form'] = InviteForm(req.user, event)
    return out

@login_required
@render_to('events/ajax/friends_invite_list.html')
def ajax_friends_invite(req, id, m_id):
    out={}
    out['event'] = event = get_object_or_404(Event, pk = id)
    out['meeting'] = meeting = get_object_or_404(Meeting, pk = m_id)

    
    if req.POST:
        out['invite_form'] = form = InviteForm(req.user, event, req.POST)
        if form.is_valid() and 'real_invite.x' in req.POST:
            users = form.cleaned_data['users']
            users = users[:]
            invities = EventInvite.objects.filter(event = event, user__in = users)
            for invite in invities:
                users.remove(invite.user)
            for user in users:
                EventInvite(
                            user = user,
                            event = event,
                            meeting = meeting,
                            who = req.user                            
                            ).save()
            req.flash.notice = ugettext('%(invited)s users successful invited') % {'invited':len(users)}
            out['invite_form'] = InviteForm(req.user, event)
    else:
        out['invite_form'] = InviteForm(req.user, event)
    return out


@login_required
@render_to('events/ajax/btn_visit_toggle.html')
def ajax_btn_visit_toggle(req, id):
    out={}
    if req.user.is_authenticated():
        out['event'] = event = get_object_or_404(Event, pk = id)
        if event.i_am_visiters():
            event.visiters.remove(req.user)
        else:
            event.visiters.add(req.user)
    return out
    


@render_to('events/one_ajax.html')
def one_ajax(req, id):
    out={}
    out['event'] = get_object_or_404(Event,Q(accept_moder=True), pk = id)
    return out

@ajax_request
def ajax_rating(req, id, ball):
    out={}
    event = get_object_or_404(Event,Q(accept_moder=True), pk = id)
    if event.can_i_set_rating():
        if event.rating(req.user, ball):
            out['value']=event.rating_percent()
        else:
            out['error'] = {'type': 405, 'message': ugettext("You can't set rating")}
    else:
        out['error'] = {'type': 405, 'message': ugettext("You can't set rating")}
    return out
#    return HttpResponseRedirect(redirect_to)

@login_required
@render_to('events/create.html')
def create(req):
    out={}
    form  = Event(accept_moder = False,author = req.user)
    if req.POST:
        out['form'] = form = CreateEventForm(req.POST, files = req.FILES,instance = form)
        if form.is_valid():
            form.save()
            req.flash.notice = ugettext('Event success added')
            return HttpResponseRedirect(form.instance.get_absolute_url())
    else:

        out['form'] = CreateEventForm(instance = form)
    return out

@login_required
@render_to('events/edit.html')
def edit(req, id, meeting_id=None):
    out={}
    out['event'] = event = get_object_or_404(Event,Q(accept_moder=True), pk = id) #, author = req.user
    if event.author != req.user and req.user not in event.assistents.all():
        raise Http404('No Events matches the given query.')
    
    form_class = EditIdeaEventForm if event.is_idea else EditAcceptedEventForm
    meeting = None
    if meeting_id:
        if int(meeting_id)==0:
            out['meeting'] = meeting = Meeting(event=event, author=req.user)
        else:            
            out['meeting'] = meeting = get_object_or_404(Meeting, pk=meeting_id, event=event)
        out['post_url'] = reverse('events_edit_meeting', args=[event.id, meeting_id])
    else:
        out['post_url'] = reverse('events_edit', args=[event.id])
        
    if req.POST:
        out['form'] = form = form_class(req.POST, files=req.FILES, instance=event)
        if meeting:
#            print "Load meeting form"
            try:
                out["end_date"] = req.POST["end_date"]
            except :
                out["end_date"] = '0'
            print out["end_date"]
            if  out["end_date"]  == '1':
                out['meeting_form'] = meeting_form = MeetingForm(req.POST, instance=meeting, prefix='meeting')
            else:
                out['meeting_form'] = meeting_form = MeetingFormNoEnd(req.POST, instance=meeting, prefix='meeting')

        if (form.is_valid() and not meeting ) or (form.is_valid() and meeting_form.is_valid()):            
            form.save()
            req.flash.notice = ugettext('Event success edited')
            if meeting:
                meeting_form.save()
                if int(meeting_id)==0: #если только что создали занчит добавить создателя в участников
                    meeting.accept_moder = False
                    meeting.visiters.add(req.user)
                    meeting.save()
                #return HttpResponseRedirect(meeting.get_absolute_url())
            
            #return HttpResponseRedirect(event.get_absolute_url())
    else:
        out['form'] = form_class(instance = event)
        if meeting:
            if meeting.end is not None:
                out["end_date"] = '1'
                out['meeting_form'] = MeetingForm(instance=meeting, prefix='meeting')
            else:
                out["end_date"] = '0'
                out['meeting_form'] = MeetingFormNoEnd(instance=meeting, prefix='meeting')
        
    return out

    
@render_to('events/visiters.html')
def visiters(req, id, page_num=None):
    out={}
    out['event'] = meeting = get_object_or_404(Meeting,Q(accept_moder=True), pk = id)
    objects = meeting.visiters.all()
    pagin=Paginator(objects, config.events_per_page())
    out['paginator']=pagin
    out['page']=page=pagin.page(int(page_num) if page_num else 1)
    return out

@login_required
@render_to('events/my_friends_visiters.html')
def my_friends_visiters(req, id, page_num=None):
    out={}
    out['event'] = event = get_object_or_404(Event,Q(accept_moder=True), pk = id)
    objects = req.user.actual_friends().filter(events_visit=event)
    pagin=Paginator(objects, config.events_per_page())
    out['paginator']=pagin
    out['page']=page=pagin.page(int(page_num) if page_num else 1)
    return out


@render_to('events/ajax/event_filter.html')
def ajax_event_filter(req):
    out={}
    return out
    
@login_required
@render_to('events/invite_list.html')
def invite_list(req, page_num):
    out={}
    out['user'] = req.user
    objects = EventInvite.objects.filter(user = req.user, deleted = False)

    pagin=Paginator(objects, config.events_per_page())
    out['paginator']=pagin
    out['page']=page=pagin.page(int(page_num) if page_num else 1)
    return out

@login_required
@render_to('events/ajax/invite_buttons.html')
def ajax_invite_action(req, id, action):
    out={}
    out['invite'] = invite = get_object_or_404(EventInvite, pk = id)
    print out
    if invite.user!=req.user:
        raise Exception("Securety exception. In invite ajax list - invite.user!=req.user")
    if action=="accept":
        if invite.accepted != True:
            invite.accepted = True            
            invite.save()

            invite.meeting.visiters.add(invite.user)
    
    if action=="reject":
        if invite.accepted != False:
            invite.accepted = False
            invite.save()
            
            invite.meeting.visiters.remove(invite.user)

    if action=="delete":
        if not invite.deleted:
            invite.deleted=True
            invite.save()
                                
    return out


@login_required
@render_to('events/photos_edit.html')
def photos_edit(req, id, page_num):
    out={}
    
    out['event'] = event = get_object_or_404(Event, pk = id)
    if event.author!=req.user and req.user not in event.assistents.all():
        return HttpResponseNotFound()
    
    objects = event.all_photo().order_by('-created')
    
    pagin=Paginator(objects, config.photo_per_page())
    out['paginator']=pagin
    out['page']=page=pagin.page(int(page_num) if page_num else 1)
    return out


@ajax_request
@login_required
def ajax_btn_photo_delete(req, photo_id):
    out={}
    photo = get_object_or_404(Photo, pk = photo_id)
    if photo.author==req.user or photo.event.author==req.user:
        photo.delete()
        out['ok']=True
    else:
        out['error'] = {'type': 405, 'message': ugettext("You can't delete photo")}
    return out
    

@login_required
@render_to("events/photo_add.html")
def photo_add(req, id):
    out={}
    out['event'] = event = get_object_or_404(Event,Q(accept_moder=True), pk = id)
#    if event.can_add_photo(req.user):
#        out['ok']=True
#        print req.POST, 
#        print req.FILES
#    else:
    if req.method=="POST":
        for file_id in req.FILES:
            file =req.FILES[file_id]
            if file:
                Photo(
                      event = event,
                      photo = file,
                      author = req.user,
                      title =req.POST.get("title_"+file_id,""),
                      ).save()
        req.flash.notice=ugettext('Photos successful added')
        return HttpResponseRedirect(event.get_absolute_url())
    return out

#@login_required
#@render_to("events/video_add.html")
#def video_add(req, id):
#    out={}
#    out['event'] = event = get_object_or_404(Event, pk = id)    
#    if req.method=="POST":
#        out['form'] = form = VideoForm(req.POST, req.FILES)
#        if form.is_valid():
#            form.instance.owner = event
#            form.save()
##        for file_id in req.FILES:
##            file =req.FILES[file_id]
##            if file:
###                Photo(
###                      event = event,
###                      photo = file,
###                      author = req.user,
###                      title =req.POST.get("title_"+file_id,""),
###                      ).save()
#            req.flash.notice=ugettext('Photos successful added')
#            return HttpResponseRedirect(event.get_absolute_url())
#    else:
#        out['form'] = VideoForm()
#    return out

@render_to("events/top.html")
def top(req, page_num=None, target=None):
    out={}
    out['target']=target
    
    #TOP for 30 days
    far_limit = datetime.datetime.today() - datetime.timedelta(30)
    
    if target=='idea':
        objects = Event.objects.filter(Q(accept_moder=True),is_idea=True).order_by('-cached_ball','-idea_rang')
    else:
        objects = Meeting.objects.for_top().filter(Q(accept_moder=True),begin__gte=far_limit).order_by('-cached_ball')
    
    pagin=Paginator(objects, config.events_per_page())
    out['paginator']=pagin
    out['page']=page=pagin.page(int(page_num) if page_num else 1)
    return out

@render_to("events/idea.html")
def idea(req, big_url=False, page_num=None, **kwargs):
    out={}
    out['big_url']=big_url
    
    if req.POST:
        out['filter'] = form = IdeaFilterForm(req.POST)
        if form.is_valid():
            return HttpResponseRedirect(form.make_url())
    else:
        out['filter'] = form =  IdeaFilterForm(initial = kwargs)


        
    objects = Event.objects.filter(Q(accept_moder=True),is_idea=True).order_by('-cached_ball','-idea_rang')
    objects = form.filter(objects)
    
    pagin=Paginator(objects, config.events_per_page())
    out['paginator']=pagin
    out['page']=page=pagin.page(int(page_num) if page_num else 1)
    return out

@render_to("events/ajax/user_events.html")
def ajax_user_events(req, id, page_num=1):
    out={}
    out['user_profile'] = user_profile = get_object_or_404(User, pk = id, is_active = True)
    objects = Event.objects.filter(author = user_profile,is_idea=False)
    
    pagin=Paginator(objects, config.events_per_user_page())
    out['paginator']=pagin
    out['ajax_url'] = reverse("ajax_user_events", args=(user_profile.id,))
    out['page']=page=pagin.page(int(page_num) if page_num else 1)
    return out


@render_to("events/ajax/user_friends.html")
def ajax_user_friends(req, id, page_num=1):
    out={}
    out['user_profile'] = user_profile = get_object_or_404(User, pk = id, is_active = True)
    objects = user_profile.actual_friends()
    
    
    pagin=Paginator(objects, config.friends_per_user_page())
    out['paginator']=pagin
    out['ajax_url'] = reverse("ajax_user_friends", args=(user_profile.id,))
    out['page']=page=pagin.page(int(page_num) if page_num else 1)
    return out

@login_required
@render_to("events/friends.html")
def friends(req, big_url=False, target=None,page_num=None, **kwargs):
    out={}
    out['big_url']=big_url
    out['target']=target
    if req.POST:
        out['filter'] = form = FriendsFilterForm(req.POST)
        if form.is_valid():
            return HttpResponseRedirect(form.make_url())
    else:
        out['filter'] = form =  FriendsFilterForm(initial = kwargs)
        
    users = User.objects.distinct().filter(is_active = True)        
    
    if req.user.is_authenticated():
        if target=="friends":
            users=users.filter(
                                 models.Q(requestor__acceptor=req.user, requestor__accepted=True)|
                                 models.Q(acceptor__requestor=req.user, acceptor__accepted=True)
                                 )

    users = form.filter(users)
 
    pagin=Paginator(users, config.friends_per_page())
    out['paginator']=pagin
    out['page']=page=pagin.page(int(page_num) if page_num else 1)
    
    return out    


@login_required
def ajax_idea_rang(req, id, sign):
    event = get_object_or_404(Event, pk = id)
    if event.can_i_set_rating():
        if sign=='+':
            event.idea_rating(req.user, +1)
        if sign=='-':
            event.idea_rating(req.user, -1)
    
    return HttpResponse("%s" % event.idea_rang)


@login_required
def make_organization(req, id):
    event = get_object_or_404(Event,Q(accept_moder=True), pk = id, state = STATE_COMPLITE)
    if event.can_i_make_organization():
        event.make_complite_to_organization()

    return HttpResponseRedirect(event.get_absolute_url())


@render_to("events/comments.html")
def comments(req, id, page_num):
    out={}
    out['event'] = event = get_object_or_404(Event,Q(accept_moder=True), pk = id)
    
    if req.POST and req.user.is_authenticated():
        out['form'] = form = CommentForm(req.POST)
        if form.is_valid():
            form.instance.event = event
            form.instance.user = req.user
            form.instance.state = event.state
            form.save()
            return HttpResponseRedirect(reverse("events_comments", args=[event.id]))
            
    else:
        out['form'] = CommentForm()
    
    objects = event.actual_comments()    
    pagin=Paginator(objects, config.comments_per_page())
    out['paginator']=pagin
    out['page']=page=pagin.page(int(page_num) if page_num else 1)
    
    return out

@login_required
def assisten_request(req, id):
    event = get_object_or_404(Event,Q(accept_moder=True), pk = id)
    AssistantRequest(user = req.user, event=event).save()
    req.flash.notice = ugettext('Request for assistant successfully sent')
    return HttpResponseRedirect(event.get_absolute_url())

@login_required
def visiter_request(req, id):
    meeting = get_object_or_404(Meeting,Q(accept_moder=True), pk = id)
    visiter = meeting.visiters.all().filter(id = req.user.id)
    if not visiter:
        meeting.visiters.add(req.user)
    else:
        meeting.visiters.remove(req.user)
        
    req.flash.notice = ugettext('Request for assistant successfully sent')
    return HttpResponseRedirect(meeting.event.get_absolute_url())


@login_required
@render_to("events/assistenrequest_list.html")
def assistenrequest_list(req):
    out={}
    if req.POST:
        print "--------------"
        print req.POST
        a = get_object_or_404(AssistantRequest, pk = req.POST['a'])
        if "yes" in req.POST:
            a.event.assistents.add(a.user)
            req.flash.notice = ugettext(u'Пользователь успешно добавлен в помощники')
            a.delete()
            return HttpResponseRedirect(reverse("assisten_list"))

        if "no" in req.POST:
            req.flash.notice = ugettext(u'Пользователь откланен')
            a.delete()
            return HttpResponseRedirect(reverse("assisten_list"))
            
    out['objects'] = AssistantRequest.objects.filter(event__author=req.user)
    return out

@login_required
@render_to("events/assisten_list.html")
def assisten_list(req):
    out={}
    out['objects'] = Event.objects.filter(Q(accept_moder=True),assistents = req.user).exclude(author=req.user)
    return out

@login_required
@render_to("events/my_events_assistan_users_list.html")
def my_events_assistan_users_list(req):
    out={}
    out['events'] = Event.objects.filter(Q(accept_moder=True),author = req.user)
    return out

@render_to("events/photo.html")
def photo(req, id):
    out={}    
    out['photo'] = photo = get_object_or_404(Photo, pk = id)
    #TODO: optimize
    cur, prev = None, None
    for next in photo.event.all_photo():
        if cur==photo:
            out['next_photo']=next
            out['prev_photo']=prev
            break            
        prev=cur
        cur=next
        
    if next==photo:
        out['next_photo']=None
        out['prev_photo']=prev        
    
    return out

@login_required()
@render_to("events/moderator_list.html")
def moderation(req):
    ret = {}
    profile = req.user.get_profile()


    if req.user.is_superuser:
        list_cat = Category.objects.all()
    else:
        list_cat = profile.user_moderation
    if not list_cat.count():
        raise Http404('No page matches the given query.')
    ret["events"] = Event.objects.filter(category__in= list_cat.all(), accept_moder=False)
    ret["ideis"] = Meeting.objects.filter(event__category__in= list_cat.all(), accept_moder=False)
    return ret

@login_required()
@render_to('events/edit.html')
def moderation_event(req, id, meeting_id=None):
    out={}
    profile = req.user.get_profile()
    if req.user.is_superuser:
        list_cat = Category.objects.all()
    else:
        list_cat = profile.user_moderation
    if not list_cat.count():
        raise Http404('No page matches the given query.')
    out['event'] = event = get_object_or_404(Event, category__in= list_cat.all(),pk = id) #, author = req.user
    if meeting_id:
        out['meeting'] = meeting = get_object_or_404(Meeting, event__category__in= list_cat.all(),pk = meeting_id) #, author = req.user
    if req.POST:

        if meeting_id:
            form2 = MeetingFormModerator(req.POST, files=req.FILES, instance=meeting)
            if form2.is_valid():
                form2.save()
                
        form = EditIdeaEventFormModerator(req.POST, files=req.FILES, instance=event)
        if form.is_valid():
            form.save()

    else:
        form = EditIdeaEventFormModerator(instance = event)
        if meeting_id:
            form2 = MeetingFormModerator(instance = meeting)
            
    out['form'] = form
    
    if meeting_id:
        out["meeting_form"] = form2


    return out