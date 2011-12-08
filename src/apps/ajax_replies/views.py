# -*- coding: utf-8 -*-
from django.views.decorators.http   import require_http_methods
from django.http                    import Http404, HttpResponse
from django.template.loader         import render_to_string
from django.core.paginator          import Paginator

from apps.ajax_replies.forms        import AddReplyForm 
#from apps.investment.models         import Company, CompanyReply,\
#                                           Project, ProjectReply 
from apps.blog.models               import Post, PostReply
#from apps.articles.models           import Articles, ArticleReply
#from apps.events.models             import Events, EventsReply 
#from apps.lib.models                import LibBook, LibBookReply

REPLIES_PER_PAGE = 10

class InvalidObjectType ( Exception ):
    pass

def fetch_replies ( object, page_num, type, request ):
    from django.utils.simplejson import dumps as _j
    paginator = Paginator ( meta_get_replies ( object, type ), REPLIES_PER_PAGE ) 
    try:
        page    = paginator.page ( page_num )
        replies = map ( lambda r: render_to_string ( 'ajax_replies/reply.html', { 'reply' : r, 'user' : request.user, 'object' : object } ), page.object_list )
        if meta_need_mark_as_not_new ( object, request.user, type ):
            for obj in page.object_list:
                if obj.is_new:
                    obj.is_new = False
                    obj.save ()
        return {
            'error_code'  : 0,
            'replies'     : replies,
            'pages_count' : len ( paginator.page_range ),
            'page_num'    : page_num,
        }
    except:
        # there is no such page
        return { 'error_code' : 2 }

@require_http_methods ( ["GET"] )
def get_replies ( request, object_id, type ):
    from django.utils.simplejson import dumps as _j
    try:
        object = meta_get_object ( object_id, type )
    except:
        # object does not exist
        return HttpResponse ( _j ( { 'error_code' : 1 } ), mimetype = 'application/json' )
    try:
        page_num = int ( request.GET [ 'page_num' ] )
        if page_num == 0:
            page_num = get_last_page_num ( object )
    except:
        page_num = get_last_page_num ( object )
    
    # fetch replies
    return HttpResponse ( _j ( fetch_replies ( object, page_num, type, request ) ), mimetype = 'application/json' )

@require_http_methods ( ["POST"] )
def add_reply ( request, object_id, type ):
    from django.utils.simplejson import dumps as _j
    if not request.user.is_authenticated ():
        return HttpResponse ( _j ( { 'error_code' : 4 } ), mimetype = 'application/json' )
    try:
        object = meta_get_object ( object_id, type )
    except:
        # object does not exist
        return HttpResponse ( _j ( { 'error_code' : 1 } ), mimetype = 'application/json' )
    form = AddReplyForm ( request.POST )
#    print "!!!!!!!!!!!=)", request.method, request.POST 
    if form.is_valid ():
#        print form.cleaned_data
        if form.cleaned_data [ "body" ].strip ():
            # save new reply
            new_reply        = meta_create_reply ( object, type )
            new_reply.author = request.user
            new_reply.body   = form.cleaned_data [ "body" ]
            new_reply.save ()
            last_page        = get_last_page_num ( object )
            # fetch replies
            return HttpResponse ( _j ( fetch_replies ( object, last_page, type, request ) ), mimetype = 'application/json' )
#    else:
#        print form.errors
    
    return HttpResponse ( _j ( { 'error_code' : 3 } ), mimetype = 'application/json' )

def get_last_page_num ( object ):
    from math import ceil
    return int ( ceil ( float ( object.replies_count ) / REPLIES_PER_PAGE ) )
    
def meta_get_replies ( object, type ):
    valid_types = {
#        'Company'  : lambda obj: CompanyReply.objects.filter ( company = obj ), 
#        'Project'  : lambda obj: ProjectReply.objects.filter ( project = obj ),
        'Post'     : lambda obj: PostReply.objects.filter ( post = obj ),
#        'Article'  : lambda obj: ArticleReply.objects.filter ( article = obj ),
#        'Events'   : lambda obj: EventsReply.objects.filter ( event = obj ),
#        'LibBook'  : lambda obj: LibBookReply.objects.filter ( book = obj ),
    }
    # verify type
    if valid_types.has_key ( type ):
        return valid_types [ type ] ( object )
    raise InvalidObjectType

def meta_get_object ( object_id, type ):
    valid_types = {
#        'Company' : lambda id: Company.objects.get ( pk = id ),
#        'Project' : lambda id: Project.objects.get ( pk = id ),
        'Post'    : lambda id: Post.objects.get ( pk = id ),
#        'Article' : lambda id: Articles.objects.get ( pk = id ),
#        'Events'  : lambda id: Events.objects.get ( pk = id ),
#        'LibBook' : lambda id: LibBook.objects.get ( pk = id ),
    }
    # verify type
    if valid_types.has_key ( type ):
        return valid_types [ type ] ( object_id )
    raise InvalidObjectType

def meta_create_reply ( object, type ): 
    valid_types = {
#        'Company' : lambda obj: CompanyReply ( company = obj ),
#        'Project' : lambda obj: ProjectReply ( project = obj ), 
        'Post'    : lambda obj: PostReply ( post = obj ),
#        'Article' : lambda obj: ArticleReply ( article = obj ),
#        'Events'  : lambda obj: EventsReply ( event = obj ),
#        'LibBook'  : lambda obj: LibBookReply ( book = obj ),
    }
    # verify type
    if valid_types.has_key ( type ):
        return valid_types [ type ] ( object )
    raise InvalidObjectType

def meta_need_mark_as_not_new ( object, user, type ):
    valid_types = {
        'Post' : lambda u: object.author == user,
    }
    if valid_types.has_key ( type ) and valid_types [ type ] ( user ):
        return True
    return False