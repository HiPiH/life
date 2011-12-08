from django.db import models
from django.utils.translation import ugettext_lazy as _

class Container(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    
    class Meta:
        pass
    
class Property(models.Model):
    container = models.ForeignKey(Container)
    name = models.CharField(max_length=255)
    value = models.TextField()
    
    class Meta:
        unique_together = ('container', 'name',)
