
from math import ceil, floor
from django.core.paginator import Page
def myPageList(self):
    if not hasattr(self,'_pageList') :
        min=self.number-5 if self.number-5>0 else 1
        max=int(ceil(float(self.paginator.count)/float(self.paginator.per_page)))    
        max=self.number+5 if self.number+5<max else max
        self._pageList = [x for x in range(min, max+1)]
    return self._pageList

Page.pageList=myPageList
Page.isOne=lambda (self): self.paginator.num_pages==1

from django.core.paginator import Paginator

Paginator.num_pagesEx=lambda (self): self.num_pages-1 