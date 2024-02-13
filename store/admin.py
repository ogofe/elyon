from django.contrib import admin
from .models import (
    Product,
    Customer,
    CustomerOrder,
    OrderItem,
    ShoppingCart
)
# Register your models here.

admin.site.register(Product)
admin.site.register(CustomerOrder)
admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(ShoppingCart)