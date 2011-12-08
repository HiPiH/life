from django import template

register = template.Library()

@register.inclusion_tag('instant_messages/tags/message_to_user.html', takes_context=True)
def message_to_user(context, user):
    #TODO: check permission to SEND user message. Replace button "Send message" to "Get a friend"
    out={
         'user': context['user'],
         'user_to': user
         }
    return out


@register.inclusion_tag('instant_messages/tags/open_im.html', takes_context=True)
def open_im(context):
    #TODO: check permission to SEND user message. Replace button "Send message" to "Get a friend"
    out={
         'user': context['user']
         }
    return out    