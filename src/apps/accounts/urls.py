from django.conf.urls.defaults import *

urlpatterns = patterns('apps.accounts.views',
    url(r'^login/$', 'login_user', name="login"),
    (r'^logout/$', 'logout_user'),
    (r'^registration/$', 'registration'),
    (r'^forgot/$', 'forgot_password'),
    
    url(r'^profile/(?P<username>[\w-]+)/$', 'profile', name="accounts_profile"),
    url(r'^myprofile/$', 'myprofile', name="myprofile"),
    
    url(r'^add/(?P<user_id>\d+)/$', 'add_friend', name="accounts_add_friend"),
    url(r'^del/(?P<user_id>\d+)/$', 'del_friend', name="accounts_del_friend"),
    url(r'^accept/(?P<user_id>\w+)/$', 'accept_friend', name="accounts_accept_friend"),
    url(r'^editprofile/$', 'profile_edit', name="accounts_profile_edit"),
    
    url(r'^myfriends/((?P<page_num>\d+).html)?$', 'myfriends', name="accounts_myfriends"),
    url(r'^(?P<username>[\w-]+)/friends/((?P<page_num>\d+).html)?$', 'user_friends', name="accounts_friends"),
    
    url(r'^myavatar/$', 'change_avatar', name="accounts_change_avatar"),
    (r'^myavatar/delete/(?P<avatar_id>\d+)/$', 'delete_avatar'),
    
    (r'^validation/$', 'validation'),
)
