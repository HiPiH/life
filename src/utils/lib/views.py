from django.http import HttpResponseRedirect
from django.contrib.comments.models import Comment

def comment_posted(request):
    if request.GET['c']:
        comment_id  = int(request.GET['c'])
        comment = Comment.objects.get(pk=int(comment_id))
        return HttpResponseRedirect(comment.content_object.get_absolute_url())

    return HttpResponseRedirect('/')