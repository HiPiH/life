
from math import ceil, floor
from django.core.paginator import Page
def my_page_list(self):
    if not hasattr(self,'_page_list') :
        min=self.number-5 if self.number-5>0 else 1
        max=int(ceil(float(self.paginator.count)/float(self.paginator.per_page)))    
        max=self.number+5 if self.number+5<max else max
        self._page_list = [x for x in range(min, max+1)]
    return self._page_list

Page.page_list=my_page_list
Page.is_one=lambda (self): self.paginator.num_pages==1

from django.core.paginator import Paginator

Paginator.num_pages_ex=lambda (self): self.num_pages-1

Paginator.in_this_page_count = lambda self: self.per_page if self.per_page<self.count else self.count 

 