from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from apps.accounts.forms import FormUserReg
from registration.views import register,activate
from apps.accounts.models import ProfileUser
from django.contrib.auth.views import  login,password_reset,logout,password_reset_confirm,password_reset_complete,password_reset_done

urlpatterns = patterns('',
    url(r'^activate/(?P<activation_key>\w+)/$',
                           activate,
                           name='registration_activate'),
    url(r'^login/$', login),
    url(r'^logout/$', logout,{"next_page":"/"}),

    url(r'^password/reset/$',
                           password_reset,{"template_name":"registration/reset.html"},
                           name='auth_password_reset'),

    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           password_reset_confirm,
                           name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$',
                           password_reset_complete,
                           name='auth_password_reset_complete'),
    url(r'^password/reset/done/$',
                           password_reset_done,
                           name='auth_password_reset_done'),

    url(r'^register/$', register,
                            {'form_class': FormUserReg,'profile_callback': ProfileUser.objects.create },
                            name='registration_register'),
    url(r'^register/complete/$',direct_to_template,
                           {'template': 'registration/registration_complete.html'},
                           name='registration_complete')
    )




urlpatterns += patterns('apps.accounts.views',
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
