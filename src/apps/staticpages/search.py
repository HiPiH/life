from apps.search import finder
from apps.staticpages.models import Page

class PageSearch(finder.ModelSearch):
    fields_list = ('title', 'content',)

finder.search_manager.register(Page, PageSearch)