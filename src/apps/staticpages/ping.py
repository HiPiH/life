import urllib, urllib2, cookielib
import httplib
import re

PING_TMPL = """<?xml version="1.0"?>
<methodCall>
  <methodName>%s</methodName>
  <params>
%s  </params>
</methodCall>
"""
PARAM_TMPL = """    <param>
      <value>%s</value>
    </param>
"""
VALUE_RTMPL = re.compile('\<name\>([^\>]*)\<\/name\>(?:.|\n|\t)*?\<value\>(?:.|\n|\t)*?\>((?:.|\n|\t)*?)\<')
#
GOOGLE_METHOD = "weblogUpdates.extendedPing"
GOOGLE_URL, GOOGLE_PAGE = "blogsearch.google.com", "/ping/RPC2"
#
YANDEX_METHOD = "weblogUpdates.ping"
YANDEX_URL, YANDEX_PAGE = "ping.blogs.yandex.ru", "/RPC2"

def postPing(url, page, body):
    res = ''
    try:
        con = httplib.HTTPConnection(url, port = 80)
        headers = {"Content-Type": "text/xml"}
        req = con.request("POST", 'http://' + url + page, body, headers)
        res = con.getresponse()
        con.close()
    except:
        pass
    return res.read() if res else ''

def ping(site_name, site_url, page_url='', rss_url='', tag_name=''):
    #google
    url, method = GOOGLE_URL, GOOGLE_METHOD
    params = ''.join(map(lambda x, pt = PARAM_TMPL: pt % x, (site_name, site_url, page_url)))
    body = PING_TMPL % (GOOGLE_METHOD, params)
    res = postPing(url, GOOGLE_PAGE, body)
    values_dict = dict(VALUE_RTMPL.findall(res))
    if not ('flerror' in values_dict.keys() and values_dict['flerror'] == '0'):
        #error
        pass
    #yandex
    url, method = YANDEX_URL, YANDEX_METHOD
    params = map(lambda x, pt = PARAM_TMPL: pt % x, (site_name, site_url, page_url))
    body = PING_TMPL % (YANDEX_METHOD, params)
    res = postPing(url, YANDEX_PAGE, body)
    values_dict = dict(VALUE_RTMPL.findall(res))
    if not ('flerror' in values_dict.keys() and values_dict['flerror'] == '0'):
        #error
        pass

#test
if __name__ == "__main__":
    ping('Official Google Blog', 'http://googleblog.blogspot.com/', 'http://googleblog.blogspot.com/')
    