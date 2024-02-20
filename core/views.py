from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .models import (
    Receivable,
    OrderUnit,
    File,
)
from store.models import (
    Customer,
    CustomerOrder,
    Product,
    Category,
    Tag,
    
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.request import HttpRequest


def generate_breadcrumbs(request):
    # Get the current path and split it into segments
    current_path = request.path_info
    path_segments = [segment for segment in current_path.split('/') if segment]

    # Build the breadcrumbs list
    breadcrumbs = []
    url_so_far = ''
    for item in range(0, len(path_segments)):
        segment = path_segments[item]
        is_last_segment = bool(segment == path_segments[-1])

        url_so_far += f'/{segment}'
        breadcrumbs.append({
            'label': segment.title(),
            'url': url_so_far,
            'active': is_last_segment
        })
    
    return breadcrumbs


def redirect_authenticated_user(route):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(route)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# Auth Views

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


# Dashboard

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


# Products Views

@login_required(redirect_field_name='rdr_next', login_url='core:login')
def product_add_view(request:HttpRequest, **kwargs):
    template = 'dashboard/products/add.html'
    categories = Category.objects.all()
    alltags = Tag.objects.all()
    receivables = Receivable.objects.all()

    ctx = {
        'active_nav': 'products',
        'page_title': 'Add New Product',
        'categories': categories,
        'tags': alltags,
        'bundles': OrderUnit.objects.all(),
        'recievables': receivables,
    }

    if request.method == "POST":
        data = request.POST
        imagelist = request.FILES.getlist('image')
        tags = data.getlist('tags')

        new_product = Product(
            name=data['name'],
            receivable=receivables.get(id=data['recievable']),
            price_per_piece=data['price'],
            price_per_bundle=data['bundle-price'],
            category=categories.get(name=data['category']),
            description=data['description']
        )
        new_product.save()

        if tags:
            for tag in tags:
                new_product.tags.add(alltags.get(name=tag),)
            new_product.save()
        
        if imagelist:
            for image in imagelist:
                img = File(
                    name=f"{new_product.slug} - image {new_product.images.count()}",
                    file=image
                )
                img.save()
                new_product.images.add(img,)
            new_product.save()
        messages.success(request, f"You added a new product {data['name']}")
        return redirect('core:products_list')
    return render(request, template, ctx)


@login_required(redirect_field_name='rdr_next', login_url='core:login')
def product_detail_view(request:HttpRequest, item_id, **kwargs):
    template = 'dashboard/products/detail.html'
    categories = Category.objects.all()
    alltags = Tag.objects.all()
    receivables = Receivable.objects.all()
    product = Product.objects.get(slug=item_id)

    ctx = {
        'active_nav': 'products',
        'page_title': f'View / Edit {product.name}',
        'categories': categories,
        'product': product,
        'tags': alltags,
        'bundles': OrderUnit.objects.all(),
        'breadcrumbs': generate_breadcrumbs(request),
        'recievables': receivables,
    }

    if request.method == "POST":
        data = request.POST
        imagelist = request.FILES.getlist('image')
        tags = data.getlist('tags')

        # new_product = Product(
        #     name=data['name'],
        #     receivable=receivables.get(id=data['recievable']),
        #     price_per_piece=data['price'],
        #     price_per_bundle=data['bundle-price'],
        #     category=categories.get(name=data['category']),
        #     description=data['description']
        # )
        # new_product.save()

        # if tags:
        #     for tag in tags:
        #         new_product.tags.add(alltags.get(name=tag),)
        #     new_product.save()
        
        # if imagelist:
        #     for image in imagelist:
        #         img = File(
        #             name=f"{new_product.slug} - image {new_product.images.count()}",
        #             file=image
        #         )
        #         img.save()
        #         new_product.images.add(img,)
        #     new_product.save()
        messages.success(request, f"You added a new product {data['name']}")
        return redirect('core:products_list')
    return render(request, template, ctx)


@login_required(redirect_field_name='rdr_next', login_url='core:login')
def products_list_view(request, **kwargs):
    template = 'dashboard/products/list.html'
    ctx = {
        'active_nav': 'products',
        'page_title': 'Product Catalog',
        'products' : Product.objects.all(),
        'breadcrumbs': generate_breadcrumbs(request)
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


# Orders View
@login_required(redirect_field_name='rdr_next', login_url='core:login')
def orders_view(request, **kwargs):
    template = 'dashboard/orders/list.html'
    
    ctx = {
        'active_nav': 'orders',
        'page_title': 'Purchase Orders',
        'orders' : CustomerOrder.objects.all(),
        'breadcrumbs': generate_breadcrumbs(request),
    }

    if request.method == "POST":
        data = request.POST
        items = data.getlist('action-item', None)
        raise Exception
    return render(request, template, ctx)



# Auxilary Views 
@login_required(redirect_field_name='rdr_next', login_url='core:login')
def receivable_create_view(request, **kwargs):
    pass


# 
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




