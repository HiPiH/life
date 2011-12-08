from django.utils.translation import ugettext

from apps.tree_comments.models import *
from apps.utils.ajax import Ajax, ajax_error
from apps.utils.templatetags.utils import _human_datetime

__all__ = ('CommentsAjax',)
 
DT_FORMAT = "%d.%m.%Y %H:%M"

class CommentsAjax(Ajax):
    pass
    
    def __comment_to_dict(self, comment):
        return {
                        'id':comment.id,
                        'text':comment.text.replace("\n","<br/>")+"<br/>",
                        'author_url':comment.author.get_absolute_url(),
                        'author':comment.author.get_full_name(),
                        'avatar':comment.author.get_avatar(),
                        'comments':comment.comments_count,
                        'created':"%s" % _human_datetime(comment.submit_date),
                        'anchor':comment.get_anchor()
                        }
    
    def get_comments(self, req, id):
        ret=[]       
        for comment in Comment.objects.filter(parent__id = id): #, published=True
            ret.append(self.__comment_to_dict(comment))
        return ret
    
    def new_comment(self, req, parent, text):
        if not req.user.is_authenticated():
            return ajax_error(403, "You not authenticated")
        
#        print "!!!!!!!!!!!!!!!!!!!!!"
#        print req.GET
#        print req.POST
        try:
            parent = Comment.objects.get(pk = parent)
        except:
            return ajax_error(404, "Can't found parent comment")

        comment = Comment(
                          content_object = parent.content_object,
                          author=req.user,
                          parent=parent,
                          text=text,
                          ip_address = req.META.get("REMOTE_ADDR", None)
                          )
        comment.save()
        return self.__comment_to_dict(comment)

        
    
        