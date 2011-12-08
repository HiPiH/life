# coding: utf-8
from django.utils.translation import ugettext_lazy as _

from apps.notifications import notify



class CommentsNotify(notify.Type):

    new_comment = notify.Method('type_name','title', 'comment', 'author', (
                    _(u"Добавлен комментарий на Ваш %(type_name)s - \"%(title)s\""),
                    _(u"""\"%(author)s\" ответил на ваш %(type_name)s - \"%(title)s\"\n\n%(comment)s""")))

    new_comment_for_comment = notify.Method('type_name','title', 'comment', 'author', (
                    _(u"Добавлен ответ на Ваш комментарий %(type_name)s - \"%(title)s\""),
                    _(u"""\"%(author)s\" ответил Вам в теме \"%(title)s\"\n\n%(comment)s""")))
    
    
    
#    def new_comment__msg(self, messenger, kwargs):
#        return (
#                _(u'Изменение в %(object_name)s::%(object_title)s Утверждено') % kwargs,  #Must approve or reject the changes
#                _(u"""%(author)s утвердил Ваши изменения в тексте.""") % kwargs)
        
        
#    comment = notify.Method('author', 'object_name', 'object_title', 'url')
#    def comment__msg(self, messenger, kwargs):
#        return (
#                _(u'Изменение в %(object_name)s::%(object_title)s Утверждено') % kwargs,  #Must approve or reject the changes
#                _(u"""%(author)s утвердил Ваши изменения в тексте.""") % kwargs)


                