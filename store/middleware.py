from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from .models import Customer, ShoppingCart
from django.contrib.auth.models import User
from django.contrib.auth import login
from .views import generate_anonymous_user_id

class CustomerCartMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.user.is_authenticated:
            if 'elyon_user_id' not in request.COOKIES:
                user_id = generate_anonymous_user_id()
                request.COOKIES['elyon_user_id'] = user_id
                response.set_cookie('elyon_user_id', user_id)
        return response
    


# class CustomerCartMiddleware(MiddlewareMixin):
#     session_id = None
#     def process_request(self, request: HttpRequest):
#         _session = request.session.session_key
#         self.session_id = _session

#         if request.user.is_anonymous:
#             customer, created = Customer.objects.get_or_create(session_id=_session)
#         else:
#             customer, created = Customer.objects.get_or_create(user=request.user)
#             # customer.user = request.user
#             # customer.save()
#             # If not authenticated, use session key to identify the customer
        
#         request.customer = customer
#         request.user_id = request.COOKIES.get('elyon-user-id', None)
#         print("Elyon User ID:", request.user_id)
    
#     def process_response(self, request: HttpRequest, response: HttpResponse):
#         if request.user.is_authenticated:
#             response.set_cookie(
#                 'elyon-user-id',
#                 request.user.username
#             )
#         elif self.session_id:
#             response.set_cookie(
#                 'elyon-user-id',
#                 self.session_id
#             )
#         else:
#             response.set_cookie(
#                 'elyon-user-id',
#                 request.session.session_key
#             )

#         return response

