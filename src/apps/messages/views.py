# coding: utf-8
"""
/-----------------------------------------------\
|   Programming by: Denis Ivanov (Doberman)     |
|   E-mail:         DenDoberman@gmail.com       |
|                   Doberman_Company@mail.ru    |
\-----------------------------------------------/
"""
from django.contrib.auth             import authenticate, login
from django.utils.translation        import ugettext as _
from django.http                     import HttpResponseRedirect
from django.shortcuts                import get_object_or_404, render_to_response
from django.contrib.auth             import logout
from django.contrib.auth.decorators  import login_required
from django.template                 import RequestContext
from django.contrib.auth.models      import User
from django.core.paginator           import Paginator
from django.template                 import Template, loader, Context
from django.core.mail                import send_mail
from django.http                     import HttpResponse
from django.template.loader          import render_to_string
from django.db.models                import Q

from apps.messages.models import UsersCommunication, MessageCommunication, FOLDERS

import random
import datetime

@login_required
def show_users_with(req, communication_id=None):
    out={}
    out['communication'] = UsersCommunication.objects.get(pk=communication_id)
    out['now_user'] = req.user
    return render_to_string('messages/template_tags/user_communication.html', out)

@login_required
def index(req, folder = 0, show=None):
    out={}
    
    if req.POST:
        if 'action' in req.POST:
            if req.POST['action'] == 'change_folder':
                if 'communication_id' in req.POST and 'to_folder' in req.POST:
                    communication_id = int(req.POST['communication_id'])
                    communication = get_object_or_404(UsersCommunication, pk=communication_id)
                    to_folder = int(req.POST['to_folder'])
                    if communication.author == req.user:
                        if communication.folder_a != to_folder:
                            communication.folder_a = to_folder
                            communication.save()
                    else:
                        if communication.folder_r != to_folder:
                            communication.folder_r = to_folder
                            communication.save()
                    return HttpResponseRedirect('/messages/%s/' % to_folder)      
                            
        
    
    folders = FOLDERS
    out['folder_now'] = folder = int(folder)
    folders_list = []
    for key, value in folders:
        AuthorOrRecipientFolder = Q(author = req.user, folder_a = int(key)) | Q(recipient = req.user, folder_r = int(key))
        communication = UsersCommunication.objects.filter(AuthorOrRecipientFolder)
        summ = 0
        summ_new = 0
        count_people = communication.count()
        for c in communication:
            if c.author == req.user:
                summ = summ + c.count_mes_a
                summ_new = summ_new + c.count_mes_a_new
            else:
                summ = summ + c.count_mes_r
                summ_new = summ_new + c.count_mes_r_new
                
        folder_add = [int(key), value.title(), int(count_people), int(summ), int(summ_new)]
        folders_list.append(folder_add)
                
    out['folders'] = folders_list

    if folder == 0 or folder == 1:
        out['show_type_links'] = 1
    
    out['show'] = show
    if show == 'new':
        AuthorOrRecipient = Q(author = req.user, count_mes_a_new__gt=0, folder_a = folder) | Q(recipient = req.user, count_mes_r_new__gt=0, folder_r = folder)
    else:
        AuthorOrRecipient = Q(author = req.user, folder_a = folder) | Q(recipient = req.user, folder_r = folder)
    communication = UsersCommunication.objects.filter(AuthorOrRecipient)
    
    for c in communication:
        c.show_users_with = show_users_with(req, c.id)
        
    out['communication'] = communication 
    
    return render_to_response('messages/index.html', out, context_instance=RequestContext(req))

@login_required
def new(req, to_user_id = None):
    out={}
    out['to_user'] = to_user = get_object_or_404(User, pk=to_user_id)
    if to_user == req.user:
        return HttpResponseRedirect('/')
    
    # НОВОЕ СООБЩЕНИЕ
    if req.POST:
        if 'action' in req.POST:
            if req.POST['action'] == 'send' and 'text' in req.POST:
                text = req.POST['text']
                if len(text) == 0:
                    out['textarea_error'] = _(u'введите текст сообщения!')
                else:
                    AuthorOrRecipient = Q(author = req.user, recipient = to_user) | Q(author = to_user, recipient = req.user)
                    try:
                        c = UsersCommunication.objects.get(AuthorOrRecipient)
                    except:
                        c = UsersCommunication(author=req.user, recipient=to_user)
                        c.save()
                    new_message = MessageCommunication(communication_to = c,
                                                       text = text,
                                                       recipient = c.author if c.recipient == req.user else c.recipient)
                    new_message.save()
                    return HttpResponseRedirect('/messages/%s/index.html' % c.id)
    
    return render_to_response('messages/new.html', out, context_instance=RequestContext(req))
    
@login_required
def list(req, communication_id = None):
    out={}
    out['LIMIT_SHOW'] = LIMIT_SHOW = 10
    # ВЫТАСКИВАЕМ СВЯЗКУ ЮЗЕРОВ ДЛЯ ОБЩЕНИЯ
    out['c'] = c = get_object_or_404(UsersCommunication, pk=int(communication_id))
    
    if c.author != req.user and c.recipient != req.user:
        return HttpResponseRedirect('/')
    
    can_sent = True
    can_sent_error = ''
    if c.author == req.user:
        if c.folder_r == 2:
             can_sent = False
             can_sent_error = u'Вы не можете написать сообщение, потому что Вас добавили в черный список'
        elif c.folder_r == 3:
             can_sent = False
             can_sent_error = u'Вы не можете написать сообщение, потому что Вас удалили из контактов'
        else:
            pass
    else:
        if c.folder_a == 2:
             can_sent = False
             can_sent_error = u'Вы не можете написать сообщение, потому что Вас добавили в черный список'
        elif c.folder_a == 3:
             can_sent = False
             can_sent_error = u'Вы не можете написать сообщение, потому что Вас удалили из контактов'
        else:
            pass
    out['can_sent'] = can_sent
    out['can_sent_error'] = can_sent_error
    
    # СПИСОК СООБЩЕНИЙ
    messages_list = MessageCommunication.objects.filter(communication_to = c)[:LIMIT_SHOW]
    
    # НОВОЕ СООБЩЕНИЕ
    if req.POST:
        if 'action' in req.POST:
            if req.POST['action'] == 'send' and 'text' in req.POST:
                text = req.POST['text']
                if len(text) == 0:
                    out['textarea_error'] = _(u'введите текст сообщения!')
                else:
                    new_message = MessageCommunication(communication_to = c,
                                                       text = text,
                                                       recipient = c.author if c.recipient == req.user else c.recipient)
                    new_message.save()
                    return HttpResponseRedirect('/messages/%s/index.html' % communication_id)
    
    # ЧТОБЫ БЫЛО ВИДНО КАКОЕ ПРОЧИТАНО КАКОЕ НЕТ :)
    for m in messages_list:
        m.is_new = m.is_read

    out['messages_list']=messages_list
    
    # ИДЕМ ПО СПИСКУ НЕ ПРОЧИТАННЫХ И ДЕЛАЕМ ИХ ПРОЧИТАННЫМИ
    for m in MessageCommunication.objects.filter(communication_to = c, is_read=False, recipient=req.user):
        m.is_new = m.is_read
        if m.recipient == req.user and m.is_read == False:
            m.is_read = True
            m.save()
            if c.author == req.user:
                if c.count_mes_a_new > 0:
                     c.count_mes_a_new = c.count_mes_a_new -1
                     c.save()
            elif c.recipient == req.user:
                if c.count_mes_r_new > 0:
                     c.count_mes_r_new = c.count_mes_r_new -1
                     c.save()
            else:
                pass
            
    return render_to_response('messages/list.html', out, context_instance=RequestContext(req))
    
@login_required
def history(req, communication_id = None, pageNum = 1):
    out={}
    out['LIMIT_SHOW_HISTORY'] = LIMIT_SHOW_HISTORY = 10
    # ВЫТАСКИВАЕМ СВЯЗКУ ЮЗЕРОВ ДЛЯ ОБЩЕНИЯ
    out['c'] = c = get_object_or_404(UsersCommunication, pk=int(communication_id))
    
    if c.author != req.user and c.recipient != req.user:
        return HttpResponseRedirect('/')
    
    # СПИСОК СООБЩЕНИЙ
    messages_list = c.messagecommunication_set.all()
    
    pagin=Paginator(messages_list, LIMIT_SHOW_HISTORY)
    out['paginator']=pagin
    out['page']=page=pagin.page(pageNum)
    
    return render_to_response('messages/history.html', out, context_instance=RequestContext(req))
    
def generator(req):
    out={}
    for i in range(50000):
        c = UsersCommunication.objects.all().order_by('?')[0]
        new_message = MessageCommunication(communication_to = c,
                                           text = u'Текст №%s' % i,
                                           recipient = c.author if i < 25000 else c.recipient)
        new_message.save()
        print u'%s из %s' % (i, 50000)
    return HttpResponseRedirect('/messages/')