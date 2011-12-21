# coding: utf-8
from apps.accounts.config import config, NEW_USERS
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, \
    AuthenticationForm
from django.contrib.auth.models import User, AnonymousUser
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, Template, loader, Context
from django.utils.translation import ugettext as _
from forms import *
from lib.shortcuts import render_to
from models import UsersAvatars, AVATAR_FROM_ADMIN, AVATAR_FROM_USERS
import datetime
import random
from apps.events.models import Event, AssistantRequest
from django.contrib.auth.forms import PasswordChangeForm,UserChangeForm

@render_to("accounts/login_user.html")
def login_user(req):
    out={}
    out['login_form'] = login_form = AuthenticationForm()
    
    if req.method == 'POST':
        out['login_form'] = login_form = AuthenticationForm(data=req.POST)
        out['login_page'] = 1
        
        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data['username'],
                password=login_form.cleaned_data['password'])
            login(req, user)
            return HttpResponseRedirect(user.get_absolute_url())
    return out

    
@login_required
def logout_user(req):
    logout(req)
    return HttpResponseRedirect('/')
    

@render_to('accounts/forgot_password.html')
def forgot_password(req):
    out={}
    # ЕСЛИ УЖЕ АВТОРИЗОВАН ТО ЧЕГО ВСПОМИНАТЬ
    if req.user.is_authenticated():
        return HttpResponseRedirect(req.user.get_absolute_url())
    
    if req.POST:
        out['forgot_form'] = forgot_form = FormUserForgot(req.POST)
        if forgot_form.is_valid():
            try:
                get_user = User.objects.get(email=forgot_form.cleaned_data['email'])
                newpassword_rand = random.randint(100000,999999)
                newpassword = "%s" % newpassword_rand
                get_user.set_password(newpassword)
                print newpassword
                ###################################
                # НАСТРОИЬТ ПОЧТУ #
                #@todo: what to do
                ###################################
                return HttpResponseRedirect("/")
            except:
                out['errbase'] = 'Ошибка базы данных...'
    else:
        out['forgot_form'] = forgot_form = FormUserForgot()
    return out
    

@render_to("accounts/registration.html")
def registration(req):
    out={}
    if req.user.is_authenticated():
        return HttpResponseRedirect(req.user.get_absolute_url())
    from registration.views import register
    return register(req,form_class=FormUserReg)

    
    # ЕСЛИ УЖЕ АВТОРИЗОВАН ТО НЕЛЬЗЯ РЕГИТЬСЯ

        
    if req.POST:
        out['reg_form'] = reg_form = FormUserReg(req.POST)
        # проверка совпадения пароля
        passworderr = None
        if req.POST['password1'] != req.POST['password2']:
            out['passworderr'] = passworderr = u'Пароли не совпадают'
            
        if reg_form.is_valid() and not passworderr:
            # СОЗДАНИЕ НОВОГО ПОЛЬЗОВАТЕЛЯ

            new_user = User.objects.create_user(reg_form.cleaned_data['username'], reg_form.cleaned_data['email'])
            new_user.first_name, new_user.last_name, new_user.birthday = reg_form.cleaned_data['first_name'], reg_form.cleaned_data['last_name'], reg_form.cleaned_data['birthday']
            new_user.metro, new_user.address, new_user.sex = reg_form.cleaned_data['metro'], reg_form.cleaned_data['address'], reg_form.cleaned_data['sex']
            
            # КОД ВАЛИДАЦИИ
            new_user.validation_code = random.randint(100000,999999)
            # УСТАНОВКА ПАРОЛЯ И СОХРАНЕНИЕ РЕАЛЬНОГО В БД
            new_user.set_password(reg_form.cleaned_data['password1'])

            if config.validation_new_users.getValue():
                new_user.is_active = False

            
            new_user.save()
            
            ###################################
            # НАСТРОИЬТ ПОЧТУ #
            #@todo: what to do
            ###################################
            """
            new_user.email_user(_('New account email confirmation'),
                   render_to_string('registration/checkemail.eml',
                                    {'new_user': reg_formUser.cleaned_data['first_name'], 'new_user_email': new_user.email, 'new_userLogin': new_user.username,
                                     'valCode': validator.code},
                                     context_instance=RequestContext(req)
                                     ),
                   from_email = SEND_FROM_EMAIL
                )
            
            # ОПОВЕЩЕНИЕ АДМИНОВ О НОВОМ ПОЛЬЗОВАТЕЛЕ
            if config.notification_admin.getValue():
            """
            
            
            if config.validation_new_users.getValue():
                return HttpResponseRedirect('/accounts/validation/')
            else:
                user = authenticate(username=reg_form.cleaned_data['username'], password=reg_form.cleaned_data['password1'])
                login(req, user)
                # Редирект юзера после регистрации, если указано NEXT
                if req.GET:
                    if 'next' in req.GET:
                        return HttpResponseRedirect(req.GET['next'])
                else:
                    return HttpResponseRedirect(new_user.get_absolute_url())                
        else:
            return out
    else:
        if req.user.is_authenticated():
            if req.GET:
                if 'next' in req.GET:
                    return HttpResponseRedirect(req.GET['next'])
            return HttpResponseRedirect(req.user.get_absolute_url())
        out['reg_form'] = reg_form = FormUserReg()
        return out
    

@render_to("accounts/validation.html")
def validation(req):
    out={}
    if req.GET:
        out['validation_form'] = validation_form = FormValidation(req.GET)
        if validation_form.is_valid():
            try:
                is_user = User.objects.get(username=req.GET['login'], validation_code=req.GET['valid_code'])
                is_user.is_active = True
                is_user.save()
                get_user_password = UsersRealPasswords.objects.get(user=is_user.id)
                user = authenticate(username=is_user.username, password=get_user_password.password)
                login(req, user)
                return HttpResponseRedirect(is_user.get_absolute_url())  
            except:
                out['message_error'] = _('No user or invalid validation code...')
    else:
        out['validation_form'] = validation_form = FormValidation()
    return out
    
@login_required
@render_to("accounts/profile.html")
def profile(req, username):
    out={}
    out['user_profile'] = user = get_object_or_404(User, username = username)
    out['is_my_profile'] = bool(req.user == user)
    if out['is_my_profile']:
        out['assistant_request'] = AssistantRequest.objects.filter(event__author=req.user).count()
        out['assistant_events'] = Event.objects.filter(assistents = req.user).exclude(author=req.user).count()
        
    
    out['in_friends'] = req.user.in_friends(user)
    out['events_created'] = user.events_author.all().count()
    out['visiters_created'] = User.objects.distinct().filter(events_visit__event__author = user).count()

    
    return out

@login_required
@render_to("accounts/profile.html")
def myprofile(req):
    out={}
    out['user_profile'] = req.user
    out['is_my_profile'] = True
    out['assistant_request'] = AssistantRequest.objects.filter(event__author=req.user).count()
    out['assistant_events'] = Event.objects.filter(assistents = req.user).exclude(author=req.user).count()
    return out
    
@login_required
@render_to("accounts/myfriends.html")
def myfriends(req, page_num=1):
    out={}
    myfriends = req.user.all_friends()
    pagin=Paginator(myfriends, config.friends_per_page())
    out['paginator']=pagin
    out['page']=page=pagin.page(int(page_num) if page_num else 1)
    return out

@login_required
@render_to("accounts/user_friends.html")
def user_friends(req, username, page_num=1):
    out={}
    out['selected_user'] = user = get_object_or_404(User, username = username)
    friends = user.actual_friends()
    pagin=Paginator(friends, config.friends_per_page())
    out['paginator']=pagin
    out['page']=page=pagin.page(int(page_num) if page_num else 1)
    return out

@login_required
def accept_friend(req, user_id):
    out={}
    if req.user.id == user_id:
        return HttpResponseNotFound
    is_user = get_object_or_404(User, pk=user_id)
    req.user.accept_friend(is_user)
    return HttpResponseRedirect(reverse("events_friends_my"))
    

@login_required
def add_friend(req, user_id):
    out={}
    if req.user.id == user_id:
        return HttpResponseNotFound
    is_user = get_object_or_404(User, pk=user_id)
    req.user.add_friend(is_user)
    return HttpResponseRedirect(reverse("events_friends_my"))
    
@login_required
def del_friend(req, user_id):
    out={}
    if req.user.id == user_id:
        return HttpResponseNotFound
    is_user = get_object_or_404(User, pk=user_id)
    req.user.delete_friend(is_user)
    return HttpResponseRedirect(reverse("events_friends_my"))

    
@login_required
@render_to("accounts/profile_edit.html")
def profile_edit(req):
    out={}
    
    if req.POST:
        out['edit_form'] = edit_form = FormUserEdit(req.POST,instance=req.user)
        edit_form.init()
        out['edit_formPass'] = edit_formPass = PasswordChangeForm(user=req.user, data=req.POST)
        # ЕСЛИ РЕДАКТИРОВАНИЕ ПРОФАЙЛА
        if 'action' in req.POST and req.POST['action'] == "%s" % 'editprofile':
            if edit_form.is_valid():
                edit_form.save()
                return HttpResponseRedirect(req.user.get_absolute_url())
                
        # ЕСЛИ СМЕНА ПАРОЛЯ
        ##########################
        # ВНИМАНИЕ!!!    НЕ ДОДЕЛАНО!!!
        #@todo: what to do
        ##########################
        if 'action' in req.POST and req.POST['action'] == 'changepass':
            if edit_formPass.is_valid():
                edit_formPass.save()
                return HttpResponseRedirect('/accounts/logout/')

    else:

        out['edit_form'] = edit_form = FormUserEdit(instance=req.user)
        edit_form.init()
        out['edit_formPass'] = edit_formPass = PasswordChangeForm(user=req.user)
        
    return out
    
@login_required
@render_to("accounts/change_avatar.html")
def change_avatar(req):
    out={}
    out['upload_form'] = upload_form = FormUploadAvatars()
    out['admin_avatars'] = UsersAvatars.objects.filter(who_upload=AVATAR_FROM_ADMIN)
    out['users_avatars'] = UsersAvatars.objects.filter(owner=req.user)
    
    if req.POST:
        if 'act' in req.POST:
            if req.POST['act'] == 'change_avatar':
                if 'thisava' in req.POST:
                    if req.POST['thisava'] == 'no':
                        ava_id = None
                    else:
                        new_ava = int(req.POST['thisava'])
                        ava_id = UsersAvatars.objects.get(pk=new_ava)
                    req.user.avatar = ava_id
                    req.user.save()
                    return HttpResponseRedirect('/accounts/myavatar/')
            elif req.POST['act'] == 'upload_avatar':
                out['upload_form'] = upload_form = FormUploadAvatars(req.POST, req.FILES)
                if upload_form.is_valid():
                    upload_form.instance.owner = req.user
                    upload_form.instance.who_upload = AVATAR_FROM_USERS
                    upload_form.save()
                    return HttpResponseRedirect('/accounts/myavatar/')
    return out
    
@login_required
def delete_avatar(req, avatar_id=None):
    if avatar_id:
        ava = UsersAvatars.objects.get(pk=avatar_id)
        ava.delete()
    return HttpResponseRedirect('/accounts/myavatar/')


def check_profile_menu_state(view_name, kwargs):
    if view_name=="apps.accounts.views.profile":
        from apps.utils.middleware.threadlocals import get_request
        req = get_request()
        if req.user.is_authenticated():
            return req.user.username==kwargs['username']

    return False


@render_to("registration/registration_complete.html")
def reg_complite(req,form=None):
    out={"form":form}
    return out