from django.contrib import admin
from .models import (
    Delivery,
    DeliveryItem,
    Receivable,
    File,
    Product,
    CustomerOrder,
    Customer,
    OrderItem,
    Invoice,
    Message,
    Notification,
    CatalogImage,
    CatalogItem,
)
# Register your models here.


admin.site.register(Delivery)
admin.site.register(DeliveryItem)
admin.site.register(Receivable)
admin.site.register(File)
admin.site.register(Product)
admin.site.register(CustomerOrder)
admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(Invoice)
admin.site.register(Message)
admin.site.register(CatalogItem)
admin.site.register(Notification)
admin.site.register(CatalogImage)