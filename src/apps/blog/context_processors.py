# -*- encoding: utf-8 -*-
from django.contrib.auth.models     import User
import operator
from apps.blog.models import Tag, PostReply, Post

def cp_all_tags(req):
    return {'cp_all_tags': sorted(Tag.objects.all().order_by('-weight')[:20], key=operator.attrgetter('name'))}

def cp_new_replies ( request ):
    replies_count = 0
    if request.user.is_authenticated () and request.user.is_blog_author:
        replies_count = PostReply.objects.filter ( post__author = request.user, is_new = True ).count ()
    return { 'cp_blog_new_replies' : replies_count }

def cp_blog_authors(req):
    authors = User.objects.filter(is_blog_author = True, is_active = True).order_by('?')[:5]
    return {'cp_blog_authors': authors}

def cp_blog_ends(req):
    return {'cp_blog_ends': Post.objects.all()[:3]}