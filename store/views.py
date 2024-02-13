from django.shortcuts import render
from django.db.models import Q
from .models import (
    Product,
    ShoppingCart,
    Customer,
    OrderItem,
    CustomerOrder,
)
from django.contrib import messages

def store_home_view(request):
    template = 'store/home.html'
    query = request.GET.get('query', None)
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__iexact=query) |
            Q(name__icontains=query)
        )

    ctx = {
        'active_nav': 'home',
        'all_products': products,
        'page_title': "Our Store",
        'searching': bool(query),
        'query': query,
    }
    return render(request, template, ctx)



def product_detail_view(request, item_id):
    template = 'store/product-detail.html'
    product: Product = Product.objects.get(slug=item_id)

    ctx = {
        'product': product,
        'page_title': "Product Detail"
    }

    if request.method == "POST":
        data = request.POST
        customer = request.customer
        item = OrderItem(
            product = product,
            quantity = data['quantity'],
            quantity_type = data['unit']
        )
        item.save()
        customer.cart.items.add(item,)
        customer.cart.save()
        messages.success(request, f"{product.name} was added to your cart")
    return render(request, template, ctx)


def cart_view(request):
    template = 'store/cart.html'
    ctx = {
        'active_nav': 'cart',
        'cart': request.cart
    }

    if request.method == "POST":
        pass
    return render(request, template, ctx)