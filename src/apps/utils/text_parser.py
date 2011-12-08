from urlparse import urlparse
import settings
import copy


try:
    from BeautifulSoup import BeautifulSoup, Tag
except:
    raise Exception("Please install BeautifulSoup")

__all__ = ('add_noindex_to_a', 'filter_html_tags', 'smart_truncate',)


def add_noindex_to_a(text):
    doc = BeautifulSoup(text)
    host_orig = urlparse(settings.SITE_URL)[1]
        
    for a in doc.findAll('a'):
        try:
            host = urlparse(a['href'])[1]
        except:
            pass
        

        if a.findParent('noindex')==None:
            if host!=host_orig:
                noindex = Tag(doc,"noindex")
                a.replaceWith(noindex)
                a['rel']='nofollow'
                noindex.insert(0,a)
    return unicode(doc)

VALID_TAGS={
    'p':[],
    'a':['href','target','rel','name'],
    'i':[],
    'u':[],
    'b':[],
    'strong':[],
    'table':['border'],
    'caption':[],
    'tbody':[],
    'thead':[],
    'tr':[],
    'th':['colspan','rowspan'],
    'td':['colspan','rowspan'],
    'noindex':[],
    'br':[],
    'blockquote':[],
    'ul':[],
    'ol':[],
    'li':[],
    'img':['src','alt','height','width','hspace','vspace','align','style'],
    'h1':[],
    'h2':[],
    'h3':[],
    'h4':[],
    'h5':[],
    'h6':[],
    'pre':[],
    'address':[],
    'div':[],
    'em':[],
}

SET_ATTR_VALUE = {
    'table':{'border':'1'}
}


def detect_page_break(tag):
    try:
        return tag.name=="div" and tag['style']=="page-break-after: always;"
    except:
        return False


def filter_html_tags(text, get_for_page_break=False):
    doc = BeautifulSoup(text)
    
    #kill all style
#    doc.findAll('style').remove()
    kill_all = False
    for tag in doc.findAll(''):
        if kill_all:
            tag.extract()
            continue
        
        if detect_page_break(tag):
            if get_for_page_break:
                kill_all=True
            tag.extract()
            continue
            
#        print "!!!!!!!!!"
#        print tag.name
        if tag.name not in VALID_TAGS:
            print "kill:",tag.name
            tag.extract()
        else:
#            print "TAG:", tag.name
#            print "    ->", tag.attrs
            #check attrs
            attrs = copy.copy(tag.attrs)
            for name,value in attrs:
                if name not in VALID_TAGS[tag.name]:
                    print "KILL ATTR %s.%s='%s'" % (tag.name, name, value)                    
                    del tag[name]
            if tag.name in SET_ATTR_VALUE:
                for attr in SET_ATTR_VALUE[tag.name]:
                    tag[attr]=SET_ATTR_VALUE[tag.name][attr]
                    
    return unicode(doc)


def smart_truncate(content, length=100, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix