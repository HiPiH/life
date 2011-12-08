# coding: utf-8
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from apps.comments.models import CommentNode, Recall
from apps.comments.forms import CommentForm
from django.contrib.auth.decorators import login_required

class CheckBan(object):
    def __init__(self, func, mess):
        self.func = func
        self.message = mess
    
    def __call__(self, req, *args, **kwargs):
        if not req.user.is_authenticated():
            if req.POST.get('next', ''):
                return HttpResponseRedirect(req.POST.get('next'))
            return HttpResponseRedirect("/")
        ban_causes = have_ban(req)
        if ban_causes:
            req.user.message_set.create(message=u"%s<br><div style='text-align: left'><ul>%s</ul></div>" % 
                                    (self.message, reduce(lambda x, y: x + "<li>%s</li>" % y , [""]+ban_causes)))
            if req.POST.get('next', ''):
                return HttpResponseRedirect(req.POST.get('next'))
            return HttpResponseRedirect("/")
        else:
            return self.func(req, *args, **kwargs)

def not_banned(mess):
    def decorator(func):
        return CheckBan(func, mess)
    return decorator

@login_required
def operate(req):
    if req.POST:
        cmt = 0
        if 'comment_on' in req.POST and req.POST['comment_on']:
            cmt = int(req.POST['comment_on'][3:])
        cm = CommentNode(author = req.user,
                         content_type = ContentType.objects.get(pk=req.POST.get('content_type')),
                         object_id = req.POST.get('object_id'),
                         body = req.POST.get('body'),
                         ip_address = req.META.get("REMOTE_ADDR", None),
                         published = True,
                         on_comment = cmt)
        try:
            cm.save()
            req.user.message_set.create(message=u"Ваш комментарий добавлен")
        except:
            req.user.message_set.create(message=u"Произошла ошибка")
    if req.POST.get('next', ''):
        return HttpResponseRedirect(req.POST.get('next'))
    return HttpResponseRedirect('/')

class EmptyStrErr(Exception):
    pass

@login_required
def operate_recall(req):
    if req.POST:
        cm = Recall(author = req.user,
                    content_type = ContentType.objects.get(pk=req.POST.get('content_type')),
                    object_id = req.POST.get('object_id'),
                    body = req.POST.get('body'),
                    published = True)
        try:
            s = req.POST.get('body')
            if not s.split():
                raise EmptyStrErr
            else:
                cm.save()
                #req.user.message_set.create(message=u"Ваш отзыв добавлен")
        except EmptyStrErr:
            req.user.message_set.create(message=u"Отзыв не может быть пустым")
        except:
            req.user.message_set.create(message=u"Произошла ошибка")
    if req.POST.get('next', ''):
        return HttpResponseRedirect(req.POST.get('next'))
    return HttpResponseRedirect(req.user.get_absolute_url())
