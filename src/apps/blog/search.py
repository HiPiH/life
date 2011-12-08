from apps.search import finder
from django.db.models import Model
import models

#for li in models.__dict__.values():
    #if type(li) == type(Model) and li.__module__ == models.__name__:
        #finder.search_manager.register(li)

class PostSearch(finder.ModelSearch):
    fields_list = ('title', 'text')

finder.search_manager.register(models.Post, PostSearch)