from django.conf.urls.defaults import *

from apps.ajax_calendar.views import ajax
from apps.events.calendar import EventsCalendar


event_list_url = '^events/(?P<string>\d+)?_(?P<date>\d{4}-\d{2}-\d{2})?_(?P<date2>\d{4}-\d{2}-\d{2})?_(?P<metro>\d+)?_(?P<category>[\w-]+)?_(?P<is_archive>\d+)?'
friend_list_url = '^users/(?P<age>\d+)?_(?P<string>[\w\W]+)?_(?P<address>[\w\W]+)?'


urlpatterns = patterns('apps.events.views',
    (r'^$', 'index'),
    url(r'^events/$', 'list', name="events_list"),
    
    url(r"%s/all/((?P<page_num>\d+).html)?$" % event_list_url,            'list', {'target':'all', "big_url":True}, name="events_list"),
    url(r"%s/my/((?P<page_num>\d+).html)?$" % event_list_url,             'list', {'target':'my', "big_url":True}, name="events_list_my"),
    url(r"%s/where_im_going/((?P<page_num>\d+).html)?$" % event_list_url, 'list', {'target':'where_im_going', "big_url":True}, name="events_list_where_im_going"),
    url(r"%s/friends/((?P<page_num>\d+).html)?$" % event_list_url,        'list', {'target':'friends', "big_url":True}, name="events_list_friends"),
    url(r"%s/friends_going/((?P<page_num>\d+).html)?$" % event_list_url,  'list', {'target':'friends_going', "big_url":True}, name="events_list_friends_going"),
    
    url(r'^users/$', 'friends', name="events_friends"),
    url(r'%s/all/((?P<page_num>\d+).html)?$' % friend_list_url, 'friends', {'target':'all', "big_url":True}, name="events_friends"),
    url(r'%s/friends/((?P<page_num>\d+).html)?$' % friend_list_url, 'friends', {'target':'friends', "big_url":True}, name="events_friends_my"),
    
#    url(r'^events/organization/$', 'list_organization', name="events_organization"),

    
#    url(r'^events/(?P<string>\d+)?_(?P<date>\d{4}-\d{2}-\d{2})?_(?P<metro>\d+)?_(?P<category>[\w-]+)?/(?P<page_num>\d+).html$', 'list'),
    
#    url(r'^events/(?P<filter_id>\d+)/$', 'list', name="events_list"),
#    url(r'^events/(?P<filter_id>\d+)/(?P<page_num>\d+).html$', 'list'),
    url(r'^events/(?P<page_num>\d+).html$', 'list'),
    
    url(r'^top/complite/((?P<page_num>\d+).html)?$', 'top', {'target':'complite'}, name="events_top_complite"),
    url(r'^top/idea/((?P<page_num>\d+).html)?$', 'top', {'target':'idea'}, name="events_top_idea"),
    
    url(r'^idea/((?P<page_num>\d+).html)?$', 'idea', {'big_url':False}, name="events_idea"),
    url(r'^idea/(?P<string>\d+)?_(?P<category>[\w-]+)?/((?P<page_num>\d+).html)?$', 'idea', {'big_url':True}, name="events_idea_filter"),
    
    
    url(r'^event/(?P<id>\d+).html$', 'one', name="events_one"),
    url(r'^event/(?P<id>\d+)_(?P<meeting_id>\d+).html$', 'one', name="events_one_meeting"),
    
    url(r'^event/(?P<id>\d+).html.ajax$', 'one_ajax'),
    url(r'^event/create.html$', 'create', name="events_create"),
    
    url(r'^event/(?P<id>\d+)/edit.html$', 'edit', name="events_edit"),
    url(r'^event/(?P<id>\d+)_(?P<meeting_id>\d+)/edit.html$', 'edit', name="events_edit_meeting"),    
    
    url(r'^event/(?P<id>\d+)/visiters.html$', 'visiters', name="event_visiters"),
    url(r'^event/(?P<id>\d+)/my_friends_visiters.html$', 'my_friends_visiters', name="event_my_friends_visiters"),
    url(r'^event/(?P<id>\d+)/photos_add.html$', 'photo_add', name="event_photo_add"),
    
    url(r'^event/invites/((?P<page_num>\d+).html)?$', 'invite_list', name="events_invite_list"),
    url(r'^event/(?P<id>\d+)/photos/((?P<page_num>\d+).html)?$', 'photos_edit', name="events_photos_edit"),
    url(r'^event/(?P<id>\d+)/make_organization.html$', 'make_organization', name="events_make_organization"),
    url(r'^event/(?P<id>\d+)/comments/((?P<page_num>\d+).html)?$', 'comments', name="events_comments"),
    
    

    
    
    
    url(r'^ajax_photo/(?P<photo_id>\d+)/delete.html$', 'ajax_btn_photo_delete', name="ajax_btn_photo_delete"),
    url(r'^ajax_event/(?P<id>\d+)/visit_toggle.html$', 'ajax_btn_visit_toggle', name="ajax_btn_visit_toggle"),
    url(r'^ajax_event/(?P<id>\d+)/(?P<m_id>\d+)/invite.html$', 'ajax_friends_invite', name='ajax_friends_invite'),
    url(r'^ajax_event/(?P<id>\d+)_(?P<ball>\d+)/rating.html$', 'ajax_rating', name='ajax_event_rating'),
    url(r'^ajax_invite/(?P<id>\d+)/accept.html$', 'ajax_invite_action', {'action':'accept'}, name='ajax_invite_action_accept'),
    url(r'^ajax_invite/(?P<id>\d+)/reject.html$', 'ajax_invite_action', {'action':'reject'}, name='ajax_invite_action_reject'),
    url(r'^ajax_invite/(?P<id>\d+)/delete.html$', 'ajax_invite_action', {'action':'delete'}, name='ajax_invite_action_delete'),
    
    url(r'^ajax_user_events/(?P<id>\d+)/((?P<page_num>\d+).html)?$', 'ajax_user_events', name='ajax_user_events'),
    url(r'^ajax_user_friends/(?P<id>\d+)/((?P<page_num>\d+).html)?$', 'ajax_user_friends', name='ajax_user_friends'),

    url(r'^ajax_idea/(?P<id>\d+)/minus.html$', 'ajax_idea_rang', {'sign':'-'}, name='ajax_idea_rang_mins'),
    url(r'^ajax_idea/(?P<id>\d+)/plus.html$', 'ajax_idea_rang', {'sign':'+'}, name='ajax_idea_rang_plus'),
    
    
    
    
    
    
    
#    url(r'^events/((?P<filter_id>\d+)/)?$', 'index', name="events_list"),

    url(r'^ajax_calendar/(?P<cur_date>\d{4}-\d{2}-\d{2})/$', ajax, kwargs={'processor_type': EventsCalendar} , name='events_ajax_calendar'),

    url(r"^assisten_request/(?P<id>\d+)/", "assisten_request", name="assisten_request"),
    url(r"^visiter_request/(?P<id>\d+)/", "visiter_request", name="visiter_request"),
    url(r"^assistenrequest_list/", "assistenrequest_list", name="assistenrequest_list"),
    url(r"^assisten_list/", "assisten_list", name="assisten_list"),
    url(r"^my_events_assistan_users_list/", "my_events_assistan_users_list", name="my_events_assistan_users_list"),


    url(r"^photo/(?P<id>\d+)/", "photo", name="events_photo"),
)
