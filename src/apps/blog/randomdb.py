# -*- coding: utf-8 -*-

from apps.data_utils      import randomize
from apps.accounts.models import User
from apps.blog.models     import Post, Tag
import datetime

def handle (  ):
    randomize.out("\ntags:")
    for i in range( 50 ):
        Tag(
            name = randomize.string(20)
            ).save()
        randomize.out('.')
    print "\nusers:",
    for i in range( 5 ):
        user, created = User.objects.get_or_create(
            username       = 'user%s' %  i ,
            email          = 'user%s@domain.com' % str( i ),        
            password       = '1q2w3e', 
            is_blog_author = True,   
            first_name     = u'Иван%s' % str( i ),
            second_name    = u'Иванович%s' % str( i ),
            last_name      = u'Иванов%s' % str ( i ),
        )
        
        if created:
            user.save ()
        
        print "\nposts"
        for j in range ( 50 ):
            post=Post (
                author          = user,
                title           = 'Post%s' % str ( i ),
                text            = 'Post text %s' % str ( i ),
                published       = True,
                enable_comments = True,
            )
            post.save ()
            if randomize.boolean():
                post.tags = Tag.objects.order_by('?')[:randomize.integer(1, 6)]
            randomize.out('.')
        randomize.out ( '.' )
        
    