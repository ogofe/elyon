from django.utils.deprecation import MiddlewareMixin
import json


class CookiesMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        url =  request.path
        if url == '/accept-cookies':
            response.set_cookie('cookie-consent', 'true')
            response.status_code = 200
            return response
        return response
    
