from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


from apps.tree_comments.ajax import CommentsAjax
from apps.tree_comments.models import Comment

ajax = CommentsAjax()

@login_required
def post(req, content_type_id, object_pk):
    ct = ContentType.objects.get_for_id(content_type_id)
    object = ct.get_object_for_this_type(pk = object_pk)
    
    if req.POST and req.POST.get('text', ''):
        #TODO: add FlashMessage to user
        parent_id = req.POST.get('parent', '')        
        parent = get_object_or_404(Comment, pk = parent_id) if parent_id else None
        comment = Comment(content_object = object,
                          author = req.user,
                          parent = parent,
                          text = req.POST.get('text', ''),
                          ip_address = req.META.get("REMOTE_ADDR", None)                          
                          )
        comment.save()
        return HttpResponseRedirect(comment.get_absolute_url())
    
    return HttpResponseRedirect(object.get_absolute_url())    