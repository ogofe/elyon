from django.shortcuts import render, redirect
from django.db.models import Q
from .models import (
    Product,
    ShoppingCart,
    Customer,
    OrderItem,
    Category,
    CustomerOrder,
)
from website.models import(
    CarouselItem
)
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
import os
from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
import uuid
# views.py


def generate_anonymous_user_id():
    return str(uuid.uuid4())


def get_or_create_customer(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        if not customer.cart:
            customer.cart = ShoppingCart.objects.create(owner=customer)
            customer.save()
    else:
        elyon_user_id = request.COOKIES.get('elyon_user_id')
        customer, created = Customer.objects.get_or_create(session_id=elyon_user_id)
        if not customer.cart:
            customer.cart = ShoppingCart.objects.create(owner=customer)
            customer.save()
            print("Customer:", customer)
        if not elyon_user_id:
            elyon_user_id = generate_anonymous_user_id()
            customer.session_id = elyon_user_id
            customer.save()
            response = redirect('signup')  # Redirect to your signup view
            response.set_cookie('elyon_user_id', elyon_user_id)
            return response
    return customer


def random_char(lim=7):
    char = os.urandom(lim).hex()
    return char

def namify_email(email:str) -> str:
    uname = email.split('@')[0]
    return uname

def login_view(request):
    template = 'store/login.html'
    rdr_next = request.GET.get('rdr_next', 'store:home')
    ctx = {
        'page_title': 'Login',
        'redirect': rdr_next,
    }
    if request.method == "POST":
        data = request.POST
        # uname = namify_email(data['email'])
        pswd = data['password']

        try:
            user = User.objects.get(email=data['email'])
            if user.check_password(pswd):
                login(request, user)
                return redirect(rdr_next)
            else:
                messages.error(request, "Invalid username / password ")
                pass
        except Exception as error:
            messages.error(request, "Invalid username / password ")
    return render(request, template, ctx)


def signup_view(request):
    template = 'store/signup.html'
    rdr_next = request.GET.get('rdr_next', 'store:home')
    ctx = {
        'page_title': 'Sign Up',
        'redirect': rdr_next,
    }
    if request.method == "POST":
        data = request.POST

        new_user = User(
            first_name = data['first_name'],
            last_name = data['last_name'],
            username = namify_email(data['email']),
            email = data['email'],
        )

        new_user.set_password(data['password'])
        new_user.save()

        customer = get_or_create_customer(request)
        customer.user = new_user
        customer.phone_number = data['phone']
        customer.save()

        login(request, new_user)
        return redirect(rdr_next)
    return render(request, template, ctx)



def store_home_view(request):
    template = 'store/home.html'
    query = request.GET.get('query', None)
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__iexact=query) |
            Q(name__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(tags__name__iexact=query) |
            Q(category__name__iexact=query) |
            Q(category__name__icontains=query) 
        )

    ctx = {
        'active_nav': 'home',
        'all_products': products,
        'page_title': "Our Store",
        'searching': bool(query),
        'categories': Category.objects.all(),
        'carousel': CarouselItem.objects.all(),
        'query': query,
    }
    return render(request, template, ctx)



def product_detail_view(request:HttpRequest, item_id):
    template = 'store/product-detail.html'
    product: Product = Product.objects.get(slug=item_id)
    customer = get_or_create_customer(request)

    ctx = {
        'product': product,
        'page_title': "Product Detail"
    }

    if request.method == "POST":
        data = request.POST
        item = OrderItem(
            product = product,
            quantity = data['quantity'],
            quantity_type = data['unit']
        )
        item.save()

        if not customer.cart:
            customer.cart = ShoppingCart.objects.create(owner=customer)
            customer.save()
        customer.cart.items.add(item,)
        customer.cart.save()
        messages.success(request, f"{product.name} was added to your cart")
    return render(request, template, ctx)


def cart_view(request:HttpRequest):
    template = 'store/cart.html'
    cart = None
    customer = get_or_create_customer(request)
    cart = customer.cart

    ctx = {
        'active_nav': 'cart',
        'cart': cart,
        'page_title': "Your Cart"
    }

    if request.method == "POST":
        data = request.POST
        item = OrderItem.objects.get(id=data['item_id'])
        product = item.product.name
        item.delete()
        messages.success(request, f"You removed {product} from your order!")
    return render(request, template, ctx)


@login_required(login_url='store:login', redirect_field_name='rdr_next')
def checkout_view(request):
    template = 'store/checkout.html'
    customer = get_or_create_customer(request)
    cart = customer.cart
    user:User = request.user

    ctx = {
        'page_title': "Place Order",
        'cart': cart,
        'customer': customer
    }
    
    if request.method == "POST":
        data = request.POST
        if not customer.phone_number:
            customer.phone_number = data['phone']
        new_order = CustomerOrder(invoiced_to=customer)
        new_order.save()
        for item in customer.cart.items.all():
            new_order.order_items.add(item,)
        new_order.save()
        messages.success(request, 'Your order has been placed!')
        return redirect('store:home')
    return render(request, template, ctx)


