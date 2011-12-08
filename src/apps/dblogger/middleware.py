# coding: utf-8
from apps.dblogger import dblogger
from django.views.debug import ExceptionReporter
import sys

class DbLoggerMiddleware(object):
    
    def process_exception(self, request, exception):
        exc_info = sys.exc_info()
        report = ExceptionReporter(request, *exc_info)
        dblogger.exception(exception, report.get_traceback_html())
