from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .models import (
    Receivable,
)
from store.models import (
    Customer,
    CustomerOrder,
    Product,
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.request import HttpRequest


def redirect_authenticated_user(route):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(route)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


@redirect_authenticated_user('core:home')
def login_view(request:HttpRequest, **kwargs):
    template = 'dashboard/accounts/login.html'
    ctx = {}
    rdr_url = request.GET.get('rdr_next', 'core:home')

    if request.method == 'POST':
        try:
            uname = request.POST['username']
            pswd = request.POST['password']
            user = User.objects.get(username=uname)

            if user.check_password(pswd):
                login(request, user)
                return redirect(rdr_url)
            else:
                # return to same page with error msg
                messages.error(request, 'Invalid username or password!')
                pass
        except Exception as error:
            messages.error(request, 'Invalid username or password!')
    return render(request, template, ctx)


def logout_view(request):
    logout(request)
    return redirect('core:login')


@login_required(redirect_field_name='rdr_next', login_url='core:login')
def home_view(request, **kwargs):
    template = 'dashboard/index.html'
    ctx = {
        'active_nav': 'index',
        'page_title': 'Dashboard',
    }
    return render(request, template, ctx)



@login_required(redirect_field_name='rdr_next', login_url='core:login')
def inventory_view(request, **kwargs):
    template = 'dashboard/inventory.html'
    ctx = {
        'active_nav': 'inventory',
        'page_title': 'Inventory',
        'inventory' : Receivable.objects.all(),
    }
    return render(request, template, ctx)


@login_required(redirect_field_name='rdr_next', login_url='core:login')
def product_add_view(request, **kwargs):
    template = 'dashboard/product-add.html'
    ctx = {
        'active_nav': 'products',
        'page_title': 'Add New Product',
    }

    if request.method == "POST":
        data = request.POST

        new_product = Product(
            # pass
        )
        new_product.save()
    return render(request, template, ctx)


@login_required(redirect_field_name='rdr_next', login_url='core:login')
def products_list_view(request, **kwargs):
    template = 'dashboard/products.html'
    ctx = {
        'active_nav': 'products',
        'page_title': 'Product Catalog',
        'products' : Product.objects.all(),
    }
    return render(request, template, ctx)



@login_required(redirect_field_name='rdr_next', login_url='core:login')
def customers_view(request, **kwargs):
    template = 'dashboard/customers.html'
    ctx = {
        'active_nav': 'customers',
        'page_title': 'Customer Records',
        'customers' : Customer.objects.all(),
    }
    return render(request, template, ctx)


@login_required(redirect_field_name='rdr_next', login_url='core:login')
def orders_view(request, **kwargs):
    template = 'dashboard/orders.html'
    
    ctx = {
        'active_nav': 'orders',
        'page_title': 'Purchase Orders',
        'orders' : CustomerOrder.objects.all(),
    }
    return render(request, template, ctx)



# @login_required('rdr_next', 'core:login')
def receivable_create_view(request, **kwargs):
    pass

def search_view(request):
    ctx = {

    }
    template = 'dashboard/search.html'
    return render(request, template, ctx)

# # @login_required('rdr_next', 'core:login')
# def inventory_view(request, **kwargs):
    # reicievable_list_view: tracks all receivables
    data = request.data
    if request.method == "POST":
        recievable = Receivable(
            name = data['name'],
            description = data['description'],
            stock_quantity = data['stock_quantity']
        )

        images = data.get('image', None)

        if images:
            for image in images:
                img = image
                recievable.images.add(img,)
            recievable.save()
        
        recievable.save()
    
    response_data = RecievableSerializer(recievable).data
    return Response(
        status=200,
        data={
            'error': False,
            'message': 'Recievable created successfully',
            'data': response_data
        }
    )