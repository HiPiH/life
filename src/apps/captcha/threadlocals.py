"""
This module allow to store thread-specific data in separate thread.
"""

from django.conf import settings

if not 'apps.captcha.threadlocals.ThreadLocalsMiddleware' in settings.MIDDLEWARE_CLASSES:
    raise Exception('You must add apps.captcha.threadlocals.ThreadLocalsMiddleware to settings.MIDDLEWARE_CLASSES if you want use threadlocals')

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

def get_request():
    """
    Return request from thread local storage.
    """

    return getattr(_thread_locals, 'request', None)


class ThreadLocalsMiddleware(object):
    """
    Middleware that save request in the thread local storage.
    """

    def process_request(self, request):
        _thread_locals.request = request

