# coding: utf-8
from apps.dblogger.models import *


def log(type, subject, content=''):
    Log(
        type = LOG_EXCEPTION,
        subject = subject[:255],
        content = content,   
        ).save()

def exception(e, content=''):
    log(LOG_EXCEPTION, unicode(e), content)
        
