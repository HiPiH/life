from apps.search import finder
from django.db.models import Model
import models

for li in models.__dict__.values():
    if type(li) == type(Model) and li.__module__ == models.__name__:
        finder.search_manager.register(li)