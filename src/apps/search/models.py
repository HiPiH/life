# -*- coding: UTF-8 -*-
# 
# This file is part of Atopowe, a Django site with phpBB integration
# Copyright (C) 2007  Maciej Bliziński
# 
# Atopowe is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# Atopowe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Atopowe; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA  02110-1301  USA
#
#
# This code was written very quickly, so it's very immature. If you have
# any comments on how to improve it, please let me know.

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site
import locale
import re

# For Python 2.3 compatibility
if not hasattr(__builtins__, 'set'):
    from sets import Set as set

class Keyword(models.Model):
    keyword = models.CharField(_('Keyword'), max_length=255,
            db_index = True, unique = True)
    def __str__(self):
        return str(self.keyword)
    class Admin:
        pass

class KeywordOccurence(models.Model):
    "Connects objects with keywords."
    keyword = models.ForeignKey(Keyword)
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField(_('object ID'), db_index = True)
    times = models.IntegerField()
    weight = models.IntegerField()
#    linked_object  = generic.GenericForeignKey('content_type', 'object_id')
    # site = models.ForeignKey(Site)
    # objects = OccurenceManager()
    class Admin:
        pass

class SearchStats(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField(_('object ID'))
    site = models.ForeignKey(Site)
