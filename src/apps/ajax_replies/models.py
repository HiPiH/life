# -*-coding: utf-8 -*-

from django.db                import models
from django.utils.translation import ugettext_lazy as _

from apps.accounts.models     import User

class Reply ( models.Model ):
    author          = models.ForeignKey ( User, verbose_name = _( u'Author' ) )
    body            = models.TextField ( _( u'Body' ) )
    adding_datetime = models.DateTimeField ( auto_now_add = True, editable = False )
    
    __unicode__     = lambda self: u'%s at %s: %s' % ( self.author, self.adding_datetime, self.body )
    
    def save ( self ):
        super ( Reply, self ).save ()
    
    class Meta:
        abstract = True
        ordering = [ 'adding_datetime' ]
