from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin
from .models import Customer, ShoppingCart
from django.contrib.auth.models import User
from django.contrib.auth import login

class CustomerCartMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest):
        _session = request.session.session_key

        if request.user.is_authenticated:
            # If authenticated, use the user's customer profile
            customer, created = Customer.objects.get_or_create(user=request.user)
            request.customer = customer
        else:
            # If not authenticated, use session key to identify the customer
            user, created = User.objects.get_or_create(username=_session)
            user.set_unusable_password()
            login(request, user)
            request.user = user
            request.customer, created = Customer.objects.get_or_create(user=user)

        if not request.customer.cart:
            # If the customer doesn't have a cart, create one
            request.cart, created = ShoppingCart.objects.get_or_create(owner=request.customer)
            request.customer.cart = request.cart

        print("Cart:", request.cart)
        print("Customer:", request.customer)
