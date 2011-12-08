
from django.db import models

class PublishedManager(models.Manager):
    def get_published(self):
        return self.get_query_set().filter(published=True)