# -*- coding: UTF-8 -*-
import re
from django.contrib.contenttypes.models import ContentType
from django.db import connection, transaction, backend, models
from apps.search.models import Keyword, KeywordOccurence
from time import time
from django.utils.http import urlquote


class ModelSearch():
    fields_list = ()
    
    def __init__(self, model, search_manager):
        
        self.model = model
        self.search_manager = search_manager
        self.HTMLtag = re.compile('<(?!(?:a\s|/a|!))[^>]*>')
        self.ct = ContentType.objects.get_for_model(self.model)
        models.signals.post_save.connect(self.index_object, sender=model)
        models.signals.post_delete.connect(self.unindex_object, sender=model)
    
    def index_model_objects(self):
        for obj in self.model.objects.all():
            self.search_manager.index_object(self.ct, obj.id, self.get_search_text(obj))
    
    def index_object(self, instance, **kwargs):
        self.search_manager.index_object(self.ct, instance.id, self.get_search_text(instance))
    
    def unindex_object(self, instance, **kwargs):
        self.search_manager.unindex_object(self.ct, instance.id)
    
    def search_model_objects(self, query):
        
        out = {}
        sviews = []
        sresult, keywords_pats = self.search_manager.search(query, self.ct)
        ids = list(set([x[0] for x in sresult]))
        for x in ids:
            obj = self.model.objects.get(pk=x)
            out = {}
            out['title'] = unicode(obj)
            out['url'] = obj.get_absolute_url()
            out['preview'] = self.make_preview(self.get_search_text(obj), keywords_pats)
            sviews.append(out)
        return sviews
    
    def get_search_text(self, obj):
        
        res = ""
        try:
            fields = [obj.__dict__[li] for li in self.fields_list] if self.fields_list else obj.__dict__.values()
        except KeyError:
            raise Exception("Invalid field name for search")
        
        for field in fields:
            if isinstance(field, (unicode, str)):
                res += " %s" % self.HTMLtag.sub('', field)
        return res
    
    def make_preview(self, s, keywords_pats):
        
        if not isinstance(s, str) and not isinstance(s, unicode):
            s2 = ""
            for weight, text in s.items():
                s2 += text + " "
            s = s2
        result = ""
        ocurences = []
        prev = 0
        for word, word_pat in keywords_pats:
            f = word_pat.search(s)
            if f:
                t = f.span()
                if prev:
                    t = t + (t[0] - prev,)
                else:
                    t = t + (0,)
                prev = t[1]
                ocurences.append(t)
        ocurences.sort()
        result = "..."
        
        def word_step(text, words, start, direction):
            f = True
            i = 0
            while f:
                if ((start+i) > 0) and ((start+i) < len(text)) and (i < 50) and (text[start+i] not in (' ', '.', ',', ';', ':')):
                    i += direction
                else:
                    if not words:
                        f = False
                    else:
                        words -= 1
                        i += direction
            return i
        
        for li in ocurences:
            st, en, distance = li
            if distance > 50:
                distance = 10
                result += "..."
                postword = word_step(s, 2, st, -1)
                result += s[st + postword: st]
            if distance == 0:
                distance = 0
                postword = word_step(s, 2, st, -1)
                result += s[st + postword: st]
            result += s[st - distance: st] + '<span style="font-weight:bold; color: Red">%s</span>' % s[st:en]
        if ocurences: 
            st, en, distance = li
            postword = word_step(s, 2, en, 1)
            result += s[en: en + postword]
        return result
    
    def search(query_string):
        print ""
        print "search"
        
        

class SearchManager():
    
    def __init__(self, *args, **kwargs):
        
        self._registry = {}
        self.words_tmpl = re.compile('\w+', re.UNICODE)
    
    def normalize(self, s):
        # Currently, this only normalizes Polish accented
        # letters. Other means of normalization such as Porter algorithm
        # for English language, can be used here.
        replace_map = {
                u'ё': u'е',
                u'й': u'и'
        }
        if type(s) != unicode:
            s = unicode(s, 'utf-8')
        s = s.lower()
        for l in replace_map.keys():
            s = s.replace(l, replace_map[l])
        return s
    
    def split_keywords(self, s):
        
        s = self.normalize(s)
        return re.findall(self.words_tmpl, s)
    
    def unindex_object(self, content_type, object_id):
        transaction.enter_transaction_management()
        transaction.managed(True)
        for ko in KeywordOccurence.objects.filter(
                content_type = content_type,
                object_id = object_id):
            ko.delete()
            del ko
        transaction.commit()
        transaction.leave_transaction_management()
    
    def keywords_dumper(self, content_type, object_id, keywords):
        if not keywords:
            return
        transaction.enter_transaction_management()
        transaction.managed(True)
        
        cursor = connection.cursor()
#        try:
        keywords = tuple(set([li.encode('utf8') for li in keywords]))
        exist_keywords = Keyword.objects.filter(keyword__in=keywords)
        keywords_in_base = tuple([li.keyword.encode('utf8') for li in exist_keywords])
        keywords_to_base = tuple(set(keywords) - set(keywords_in_base))
        
        if keywords_to_base:
            sql_exist_keywords = "insert into search_keyword (keyword) values "+\
            ", ".join(map(lambda li: "('%s')" % li, keywords_to_base))+\
            ";\n"
            cursor.execute(sql_exist_keywords)
                    
            exist_keywords = Keyword.objects.filter(keyword__in=keywords)
            keywords_ids = [li.id for li in exist_keywords]
        
#TODO нужно оптимизировать - добавлять только новые
            sql_delete_occurences = "delete from search_keywordoccurence where content_type_id = %d and object_id = %d;\n" % (content_type.id, object_id)
            cursor.execute(sql_delete_occurences)
            
            #TODO Почему то не используеться  times, weight  или я что-то не понял =(
            sql_insert_occurences = "insert into search_keywordoccurence (keyword_id, content_type_id, object_id, times, weight) values "+\
            ", ".join(map(lambda li: "(%d, %d, %d, %d, %d)" % (int(li), content_type.id, object_id, 1, 1), keywords_ids))+\
            ";\n"
            cursor.execute(sql_insert_occurences)
            
        
        transaction.commit()
        transaction.leave_transaction_management()
#        except Exception, e:
#            print "******* Exception:", e
#            transaction.rollback()
#            print connection.queries[-1]
    
    def index_object(self, content_type, object_id, text_to_index):
        
        keywords = self.split_keywords(text_to_index)
        self.keywords_dumper(content_type, object_id, keywords)
        
    def search(self, query, content_type=None):
        
        keywords = self.split_keywords(query)
        # change ['a', 'b', 'c'] into [(1, 'a'), (2, 'b'), (3, 'c')]
        # keyword-index-pairs
        kwips = [x for x in enumerate(keywords)]
        print keywords
        print kwips
        # print kwips
        clauses = {}
        # Construct the query
        clauses['select'] = " ".join([" ko%d.object_id AS object_id%d, ko%d.content_type_id As content_type_id%d,\n" % ((x[0],)*4) for x in kwips])
        clauses['select'] += "\n".join(["sk%d.keyword AS kw%d,\n" % ((x[0],)*2) for x in kwips])
        clauses['select'] += "\n".join(["ko%d.times AS times%d," % ((x[0],)*2) for x in kwips])
        clauses['select'] += " + ".join(["ko%d.times" % x[0] for x in kwips])
        clauses['select'] += " AS sum_times, "
        clauses['select'] += " + ".join(["ko%d.weight" % x[0] for x in kwips])
        clauses['select'] += " AS sum_weights"
        clauses['from'] = "\n".join(["search_keyword AS sk%d," % x[0] for x in kwips])
        clauses['from'] += ",\n".join(["search_keywordoccurence AS ko%d" % x[0] for x in kwips])
        clauses['where'] = " AND ".join([" sk%d.keyword like %%s \n" % x[0] for x in kwips])
        clauses['where'] += "\n".join([" AND sk%d.id = ko%d.keyword_id" % ((x[0],)*2) for x in kwips])
        if content_type:
            clauses['where'] += "\n".join([" AND ko%d.content_type_id = %s\n" % (x[0], content_type.id) for x in kwips])
        if len(kwips) > 1:
            clauses['where'] += "\n".join([" AND ko%d.object_id = ko%d.object_id\n" % (x[0] - 1, x[0]) for x in kwips[1:]])
            clauses['where'] += "\n".join([" AND ko%d.content_type_id = ko%d.content_type_id\n" % (x[0] - 1, x[0]) for x in kwips[1:]])
        clauses['order_by'] = 'sum_weights DESC, sum_times DESC'
        qry = """
SELECT
    %(select)s
FROM
    %(from)s
WHERE
    %(where)s
ORDER BY
    %(order_by)s
LIMIT
    10
;
        """ % clauses
        
        print qry
        
        cursor = connection.cursor()
        cursor.execute(qry, tuple(["%s%%" % li for li in keywords]))
        res = cursor.fetchall()
        keywords_pats = map(lambda x: (x, re.compile(x, re.IGNORECASE|re.UNICODE)), keywords)
        return res, keywords_pats
    
    def search_ex(self, query, content_type=None):
        pass
        
    
    def index_all(self):
        st = time()
        for li in self._registry.values():
            li.index_model_objects()
        en = time()
        print str(en-st)
    
    def search_all(self, query):
        
        sviews = []
        for li in self._registry.values():
            sviews.extend(li.search_model_objects(query))
        return sviews
    
    def search_for_model(self, query, model):
        if model in self._registry.keys():
            return self._registry[model].search_model_objects(query)
        return []
    
    def get_models(self):
        return self._registry.keys()
    
    def register(self, model, search_class=None):
        
        if not search_class:
            search_class = ModelSearch
        if model in self._registry:
            return 
        
        self._registry[model] = search_class(model, self)
        
    def filter(self, query_set, keywords):
        keywords = self.split_keywords(keywords)
        
        qs = models.Q()
        for word in keywords:
            qs = qs | models.Q(keywordoccurence__keyword__keyword__contains = word)
            
        return query_set.filter(qs)
    
    def keywords_to_url(self, s):
        return urlquote(" ".join(self.split_keywords(s)))

search_manager = SearchManager()

def autodiscover():
    from settings import INSTALLED_APPS
    for apps in INSTALLED_APPS :
        mod = __import__(apps, globals(), locals(), ['search'])
