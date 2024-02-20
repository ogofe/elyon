from django.urls import path
from .views import (
    home_view,
    login_view,
    logout_view,

    # products
    product_add_view,
    products_list_view,
    product_detail_view,

    inventory_view,
    customers_view,
    orders_view,

    search_view,
)


app_name = 'core'


urlpatterns = [
    path('', home_view, name='home'),
    path('search/', search_view, name='search'),
    
    path('products/add/', product_add_view, name='product_add'),
    path('products/<item_id>/', product_detail_view, name='product_detail'),
    path('products/', products_list_view, name='products_list'),
    
    path('customers/add/', customers_view, name='customers_list'),
    path('customers/<customer_id>/', customers_view, name='customers_list'),
    path('customers/', customers_view, name='customers_list'),

    path('inventory/add/', inventory_view, name='inventory_add'),
    path('inventory/<item_id>/', inventory_view, name='inventory_detail'),
    path('inventory/', inventory_view, name='inventory_list'),

    path('staff/add/', products_list_view, name='staff_add'),
    path('staff/<staff_id>/', products_list_view, name='staff_detail'),
    path('staff/', products_list_view, name='staff_list'),

    path('orders/add/', orders_view, name='order_add'),
    path('orders/<order_id>/', orders_view, name='order_detail'),
    path('orders/', orders_view, name='order_list'),
    
    path('deliveries/', products_list_view, name='deliveries_list'),
    
    path('messages/<message_id>/', products_list_view, name='messages'),
    path('messages/', products_list_view, name='messages_detail'),

    path('notifications/<notification_id>/', products_list_view, name='alerts'),
    path('notifications/', products_list_view, name='alert_detail'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', login_view, name='register'),
]
