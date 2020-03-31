# coding: utf-8
from threading import local

_thread_locals = local()


def get_current_request():
    """ returns the request object for this thread """
    return getattr(_thread_locals, "request", None)


def get_current_user():
    """ returns the current user, if exist, otherwise returns None """
    request = get_current_request()
    if request:
        return getattr(request, "user", None)


class GlobalRequestMiddleware(object):
    """ Simple middleware that adds the request object in thread local storage."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request

        response = self.get_response(request)

        if get_current_request():
            try:
                del _thread_locals.request
            except AttributeError:
                pass
        return response
