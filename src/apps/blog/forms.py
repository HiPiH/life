# -*- encoding: utf-8 -*-
from django import forms
from apps.blog.models import Post, Tag
from apps.utils.widgets import AdminDateTimeWidget
from django.utils.translation import ugettext_lazy as _
from apps.utils.forms              import CustomForm, CustomModelForm

class Textarea(forms.Textarea):
    def __init__(self, attrs=None):
        super(forms.Textarea, Textarea).__init__(self)
        if attrs:
            self.attrs.update(attrs)

class TagsFileld(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(TagsFileld, self).__init__(*args, **kwargs)
    def clean(self, value):
        # todo: real clean
        return super(TagsFileld, self).clean(value)

class PForm(CustomModelForm):
    #teaser = forms.CharField(label=_(u'post teaser').capitalize(), widget=Textarea({'style': "width: 100%", 'rows': '7'}))
    text = forms.CharField(label=_(u'text').capitalize(), widget=Textarea({'style': "width: 100%", 'rows': '20'}))
    tags = TagsFileld(label=_(u'tags').capitalize(), required=False,  help_text=_('insert comma separated tags'))
    class Meta:
        model = Post
        fields = ('title', 'text', 'published', 'enable_comments')

class PostForm(PForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.initial['tags'] = self.instance.tagstring
    
    def get_tags(self):
        tags = self.instance.tags.all()
        return ", ".join(map(lambda x: x.name, tags))
    
    def save(self, commit=True):
        if self.instance.pk is None:
            fail_message = 'created'
        else:
            fail_message = 'changed'
        newinst = forms.save_instance(self, self.instance, self._meta.fields, fail_message, commit)
        # processim tagi
        tags = filter(None, map(lambda x: x.strip().lower(), self.cleaned_data['tags'].split(',')))
        tags = tuple(set(tags))
        newinst.tagstring = ', '.join(tags)
        if not newinst.published:
            # просто сохраняем строку
            hastags = newinst.tags.all()
            for tag in hastags:
                if tag.weight <= 1:
                    tag.delete()
                else:
                    tag.weight -= 1
                    tag.save()
                    tag.post_set.remove(newinst)
        else:
            hastags = map(lambda x: x.name, newinst.tags.all())
            tags_to_delete = list(set(hastags) - set(tags))
            for li in tags_to_delete:
                tag = Tag.objects.get(name=li)
                if tag.weight <= 1:
                    tag.delete()
                else:
                    tag.weight -= 1
                    tag.save()
                    tag.post_set.remove(newinst)
            for li in tags:
                if li not in hastags:
                    tag, cr = Tag.objects.get_or_create(name=li)
                    newinst.tags.add(tag)
                    if not cr:
                        tag.weight += 1
                        tag.save()
        newinst.save()
        return newinst