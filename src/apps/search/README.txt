-*- coding: UTF-8 -*-

== Search for Django ==

This is an implementation of an search engine, using purely Django
framework. It is intended to work with all Django-supported database backends.
It provides very basic indexing and search capabilities, using a simple API.
Implementation of the search is inspired by comments framework for Django.

== Prerequisites ==

Django, http://www.djangoproject.com/

== INSTALL ==

Currently, the code is available only from a Subversion repository.

svn checkout http://www.atopowe-zapalenie.pl/portalatopowe/branches/search/search/

This address is temporary, it will probably change in the future (this
file will be then updated).

To make search available from Django, put it into django/contrib or link
it there. Assuming that Search code is in /home/joe/search and Django
source code is in /home/joe/django_src, you can:

ln -s /home/joe/search /jome/joe/django_src/django/contrib

== API ==

Objects to be indexed need to implement two methods:

get_search_text() and get_absolute_url()

Objects will be indexed by whatever text get_search_text() returns. The
second method will be used to create hyperlinks in the results.

Here's an example Django code, for indexing:

from myapp.models import MyClass
from django.contrib.search.models import Keyword
from django.contrib.contenttypes.models import ContentType

ct = ContentType.objects.get_for_model(MyClass)
t = MyClass.objects.get(pk = 1)
Keyword.objects.index_object(ct, t.topic_id)

...and for searching:

from django.contrib.search.models import KeywordManager
from django.contrib.contenttypes.models import ContentType
from myapp.models import MyClass
ct = ContentType.objects.get_for_model(MyClass)
km = KeywordManager()
result = km.search(ct, "Monty Python")
print result

[{'url': '/path/object/',
 'preview': 'preview of the object content',
 'title': 'Object title' },
 { ... }, ... ]

Results are a list of dictionaries where each dictionary has fields:
url, preview and title.


Search is written by Maciej Bliziński, <maciej.blizinski@gmail.com>
Comments are welcome!
