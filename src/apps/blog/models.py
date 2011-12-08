# -*- encoding: utf-8 -*-
# clear
import re
from datetime import time as t, date as d, datetime as dt
from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.db.models import permalink
from django.contrib.contenttypes.models import ContentType
from django.utils import html
from apps.utils.managers import PublishedManager
from apps.comments.models import CommentNode


#class Config(property.Container):
    #_title = _('Blog config')
    #comments_exp_days = property.Int(default = 0, title=_('comments expire days'))
#config = Config()

#class Section(models.Model):
#    title = models.CharField(_('section title'), max_length=255)
#    description = models.TextField(_(u'section description'), blank=True)
#    post_count = models.PositiveIntegerField(default=0, editable=False)
#    
#    __unicode__ = lambda self: u'%s' % self.title
#    
#    class Meta:
#        verbose_name        = _(u'section')
#        verbose_name_plural = _(u'sections')
#
#    @permalink
#    def get_absolute_url(self):
#        return ('section', [self.id])

from apps.ajax_replies.models import Reply

class PostReply ( Reply ):
    post   = models.ForeignKey ( 'Post', verbose_name = _( u'Запись' ) )
    is_new = models.BooleanField ( default = True, editable = False )
    
    class Meta ( Reply.Meta ):
        verbose_name        = _( u'Комментарий к записи' )
        verbose_name_plural = _( u'Комментарии к записи' )
        
    def save ( self ):
        if not self.id:
            self.post.replies_count += 1
            self.post.save ()
            if self.author == self.post.author:
                self.is_new = False
        super ( PostReply, self ).save ()
        
    def delete ( self ):
        self.post.replies_count -= 1
        self.post.save ()
        super ( PostReply, self ).delete ()
    
class Tag(models.Model):
    name = models.CharField(_('tag name'), max_length=255)
    weight = models.PositiveIntegerField(_('tag weight'), default=1)
    
    __unicode__ = lambda self: u'%s' % self.name
    
    class Meta:
        verbose_name        = _(u'tag')
        verbose_name_plural = _(u'tags')
    
    @permalink
    def get_absolute_url(self):
        return ('tag', [self.id])
    
class Post(models.Model):
    title = models.CharField(_(u'post title'), max_length=255)
    author = models.ForeignKey(User, verbose_name=_(u'author'), related_name='posts')
    slug = models.SlugField(_(u'slug'), max_length=255, blank=True, unique_for_date="date", editable=False)
    text = models.TextField(_(u'text'))
    date = models.DateTimeField(_(u'date'), default=dt.now, editable=False)
    published = models.BooleanField(verbose_name=_(u'post published'), default=True)
    enable_comments = models.BooleanField(verbose_name=_(u'enable comments'), default=True)
#    section = models.ManyToManyField(Section, verbose_name=_(u'sections'), blank=True, null=True)
    tags = models.ManyToManyField(Tag, verbose_name=_(u'tags'), blank=True, null=True)
    last_post = models.BooleanField(default=False, editable=False)
    tagstring = models.CharField(max_length=255, default="", editable=False)
#    featured = models.BooleanField(default=False, editable=False)
    comments_count = models.PositiveIntegerField(default=0, editable=False)
    commentnode = generic.GenericRelation(CommentNode)
    new_comments = models.BooleanField(default=False, editable=False)
    published_posts = PublishedManager()
    objects = models.Manager()
    
    replies_count = models.PositiveIntegerField ( default = 0, editable = False )
    
    views_count = models.PositiveIntegerField ( default = 0, editable = False )
    
    class Meta:
        ordering = ['-date', 'author', ]
        get_latest_by = 'date'
        verbose_name        = _(u'post')
        verbose_name_plural = _(u'posts')
    
    def __unicode__(self):
        return '"%s"' % self.title
    
    @permalink
    def get_absolute_url(self):
        return ('blog_post_detail', [self.author.username, self.date.strftime("%Y-%m-%d"), self.slug])
    
    @permalink
    def get_url_to_edit(self):
        return ('blog_edit_post', [self.author.username, self.date.strftime("%Y-%m-%d"), self.slug])
    
    @permalink
    def get_url_to_delete(self):
        return ('blog_delete_post', [self.author.username, self.date.strftime("%Y-%m-%d"), self.slug])
    
    def published_comments(self):
        return self.get_comments().filter(published=True)
    
    def get_comments(self):
        return self.commentnode.all().order_by('path', 'pub_date')
    
    def comments_open(self):
        exp_days = 0 #config.comments_exp_days.getValue()
        if exp_days:
            return self.enable_comments and (datetime.today() - timedelta(exp_days)) <= self.date
        else:
            return self.enable_comments
    comments_open.boolean = True

    def get_announce(self):
        #tmpl_hr = re.compile(r'\<hr[^\/]*\/\>')
        #tmpl_div_start = re.compile(r'\<div')
        #tmpl_div_end = re.compile(r'\<\/div')
        #hr_match = tmpl_hr.search(self.text)
        #if hr_match:
            #teaser, body = tmpl_hr.split(self.text, 1)
        #else:
            #teaser = self.text
        return html.strip_tags(self.text)[:300]
    
    def save(self):
        if not self.id:
            self.last_post=True
            Post.objects.filter(last_post=True, author = self.author).update(last_post=False)
            
        if not self.slug:
            from pytils.translit import slugify
            # verify
            today = (dt.combine(dt.now(), t.min), dt.combine(dt.now(), t.max))
            slug = slugify(self.title)[:50]
            slug_count = Post.objects.filter(date__range=today, author=self.author, slug__istartswith=slug).count()
            self.slug = slug + str(slug_count+1) if slug_count else slug
        super(Post, self).save()
        
    def delete(self):
        tags = self.tags.all()
        for tag in tags:
            if tag.weight <= 1:
                tag.delete()
            else:
                tag.weight -= 1
                tag.save()
                #tag.post_set.remove(newinst)
        super(Post, self).delete()

def get_new_commented_posts(self):
    return Post.published_posts.filter(author=self, new_comments=True)

User.get_new_commented_posts = get_new_commented_posts

def get_last_posts(self):
    return Post.published_posts.filter(author=self).order_by('-date')[:10]

User.get_last_posts = get_last_posts


@models.permalink
def get_blog_absolute_url ( self ):
    return ( 'blog_post_list', [], { 'author' : self.username } )
User.get_blog_absolute_url = get_blog_absolute_url


User.add_to_class ( 'is_blog_author', models.BooleanField ( _(u'Это автор блога?'), default=False ))
AnonymousUser.is_blog_author = False
