# coding: utf-8
import time
import re
import operator
from datetime import time as t, date as d, datetime as dt
from django.shortcuts import get_object_or_404, render_to_response, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
import datetime

from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from lib.shortcuts import render_to

from apps.blog.models import Post, PostReply, CommentNode, Tag
from apps.blog.forms import PostForm

from settings import SITE_NAME, SITE_ADDRESS

from apps.blog.config import config

POSTS_ON_PAGE = 20

@login_required
@user_passes_test ( lambda u: u.is_blog_author )
def new_replies ( request ):
    posts = Post.objects.filter ( author = request.user )
    rs    = []
    for post in posts:
        new_replies = PostReply.objects.filter ( post = post, is_new = True )
        if new_replies:
            rs.append ( { 'post' : post, 'replies' : new_replies } )
    return render_to_response ( 'blog/new_replies.html', { 'rs' : rs }, RequestContext ( request ) )

def _get_reply_to(request):
    try:
        return int(request.GET.get('reply_to', None))
    except (ValueError, TypeError):
        return None

def get_tags():
    return sorted(Tag.objects.all().order_by('-weight')[:20], key=operator.attrgetter('name'))

def get_posts(keywords):
    return Post.objects.filter(**keywords).order_by('-date')

def index(req, page_num = None):
    page_num = 1 if not page_num else page_num
    out = {}
    keywords = {'published': True, }
    out['pager'] = Paginator(get_posts(keywords), POSTS_ON_PAGE)
    out['page'] = out['pager'].page(page_num)
#    out['sections'] = Section.objects.all()
    out['tags'] = get_tags()
    out['ctype'] = ContentType.objects.get_for_model(Post).id
    
    return render_to_response("blog/index.html", out, RequestContext(req))

#def section(req, sectID, page_num):
#    page_num = 1 if not page_num else page_num
#    out = {}
#    keywords = {'section__id': sectID, 'published': True}
#    out['pager'] = Paginator(get_posts(keywords), POSTS_ON_PAGE)
#    out['page'] = out['pager'].page(page_num)
#    sections = Section.objects.all()
#    out['tags'] = get_tags()
#    out['cur_section'] = filter(lambda x, sid=int(sectID): not cmp(x.id, sid), sections)[0]
#    out['sections'] = sections
#    return render_to_response("blog/index.html", out, RequestContext(req))

def tag(req, tagID, page_num):
    page_num = 1 if not page_num else page_num
    out = {}
    keywords = {'tags__id': tagID, 'published': True}
    out['pager'] = Paginator(get_posts(keywords), POSTS_ON_PAGE)
    out['page'] = out['pager'].page(page_num)
#    out['sections'] = Section.objects.all()
    tags = get_tags()
    out['cur_tag'] = filter(lambda x, tid = int(tagID): not cmp(x.id, tid), tags)[0]
    out['tags'] = tags
    return render_to_response("blog/index.html", out, RequestContext(req))

def post_list(req, author, page_num):
    out = {}
    out['author'] = author = get_object_or_404(User, username=author)

    page_num = 1 if not page_num else page_num
    if req.user == author:
        out['validuser'] = req.user
        posts = Post.objects.filter(author = author)
    else:
        posts = Post.objects.filter(published=True, author = author)
    out['pager'] = Paginator(posts, POSTS_ON_PAGE)
    out['page'] = out['pager'].page(page_num)
    
    out['back_link'] = '/blog/'
    
    out['tags'] = get_tags()
    
    return render_to_response("blog/post_list.html", out, RequestContext(req))

def _get_date(date_str):
    try:
        return d(*time.strptime(date_str, '%Y%m%d')[:3])
    except ValueError:
        raise Http404

def post_detail(req, author, date, slug):
    reply_to = _get_reply_to(req)
    date = d(*time.strptime(date, '%Y-%m-%d')[:3])
    today = (dt.combine(date, t.min), dt.combine(date, t.max))
    post = get_object_or_404(Post.objects.filter(date__range=today), slug=slug, author__username=author)
    post.views_count = post.views_count + 1
    post.save()
    
    out = {}
    if req.user.username == author:
        out['validuser'] = req.user
        post.new_comments = False
        post.save()
    
    out.update({
            'post': post,
            'reply_to': reply_to,
            'site': Site.objects.get_current(),
            'post_detail':True})
    out['back_link'] = "/blog/posts/%s/" %author
    out['author'] = User.objects.get(username=author)
        
    from apps.ajax_replies.forms import AddReplyForm
    
    out [ 'ajax_replies_add_form' ] = AddReplyForm()
    
    out['tags'] = get_tags()
    
    return render_to_response('blog/post_detail.html', out, RequestContext(req))

def last_posts(req, author):
    lposts = Post.published_posts.order_by("-date")
    return render_to_response("blog/post_list.html", {'posts': lposts}, RequestContext(req))

def friends_last_posts(req, author):
    if isinstance(req.user, AnonymousUser):
        return HttpResponseRedirect('/blog/')
    else:
        fposts = Post.published_posts.filter(author__in = req.user.friends.all()).order_by("-date")
    return render_to_response("blog/post_list.html", {'posts': fposts}, RequestContext(req))

@login_required
def create_post(req, author):
    out={}
    out['author'] = author = get_object_or_404(User, username=author)
    out['back_link'] = reverse("blog_post_list", args=[author])
    if req.POST:
        pm = Post(author = req.user)
        out['form'] = form = PostForm(req.POST, instance = pm)
        if form.is_valid():
            form.save()
            last_post = Post.objects.filter(author=pm.author, last_post=True)
            if last_post:
                last_post = last_post[0]
                last_post.last_post = False
                last_post.save()
            post_ldate = Post.objects.filter(author=pm.author, published=True).order_by('-date')
            if post_ldate:
                post_ldate = post_ldate[0]
                post_ldate.last_post = True
                post_ldate.save()
            return HttpResponseRedirect ( req.user.get_blog_absolute_url () )
    else:
        out['form'] = PostForm()
        
    return render_to_response('blog/createPost.html', out, RequestContext(req))

@login_required
def edit_post(req, author, date, slug):
    redirect_to = reverse("blog_post_list", args=[author])
    date = d(*time.strptime(date, '%Y-%m-%d')[:3])
    today = (dt.combine(date, t.min), dt.combine(date, t.max))
    post = get_object_or_404(Post.objects.filter(date__range=today), slug=slug, author__username=author)
    if req.user != post.author and not req.user.is_superuser:
        return HttpResponseRedirect(redirect_to)
    form = PostForm(instance = post)
    if req.POST:
        form = PostForm(req.POST, instance = post)
        if form.is_valid():
            ps = form.save()
            last_post = Post.objects.filter(author=ps.author, last_post=True)
            if last_post:
                last_post = last_post[0]
                last_post.last_post = False
                last_post.save()
            post_ldate = Post.objects.filter(author=ps.author, published=True).order_by('-date')
            if post_ldate:
                post_ldate = post_ldate[0]
                post_ldate.last_post = True
                post_ldate.save()
            return HttpResponseRedirect(redirect_to)
    return render_to_response('blog/createPost.html', {'form': form, 'back_link': redirect_to, 'is_edit': 1}, RequestContext(req))

@login_required
def delete_post(req, author, date, slug):
    redirect_to = reverse("blog_post_list", args=['author'])
    date = d(*time.strptime(date, '%Y-%m-%d')[:3])
    today = (dt.combine(date, t.min), dt.combine(date, t.max))
    post = get_object_or_404(Post.objects.filter(date__range=today), slug=slug, author__username=author)
    if req.user != post.author and not req.user.is_superuser:
        return HttpResponseRedirect(redirect_to)
    comments = post.get_comments()
    if req.POST and u'delete' in req.POST.keys():
        post.delete()
        last_post = Post.objects.filter(author=req.user, last_post=True).exclude(id=post.id)
        if last_post:
            last_post = last_post[0]
            last_post.last_post = False
            last_post.save()
        post_ldate = Post.objects.filter(author=req.user, published=True).exclude(id=post.id).order_by('-date')
        if post_ldate:
            post_ldate = post_ldate[0]
            post_ldate.last_post = True
            post_ldate.save()
        return HttpResponseRedirect(redirect_to)
    return render_to_response("blog/delete_confirm.html", 
                              {'post': post, 'comments': comments, 'back_link': redirect_to }, RequestContext(req))


@render_to('blog/authors.html')
def authors(req, page_num=None):
    out={}
    authors = User.objects.filter( is_active = True)
    out['paginator']=pagin=Paginator(authors, config.authors_per_page())
    out['page']=page=pagin.page(int(page_num) if page_num else 1)
    return out


@render_to('blog/ajax/user_posts.html')
def ajax_user_posts(req, id, page_num):
    out={}
    out['user_profile'] = user_profile = get_object_or_404(User, pk = id, is_active = True)
    objects = Post.objects.filter(published=True, author = user_profile)

    
    pagin=Paginator(objects, config.posts_per_user_page())
    out['paginator']=pagin
    out['ajax_url'] = reverse("blog_ajax_user_posts", args=(user_profile.id,))
    out['page']=page=pagin.page(int(page_num) if page_num else 1)
    return out