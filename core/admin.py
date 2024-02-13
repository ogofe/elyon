from django.contrib import admin
from .models import (
    ShipmentDelivery,
    ShipmentItem,
    Receivable,
    File,
    Message,
    Notification,
    OrderUnit,
    SiteSettings,
)
# Register your models here.


admin.site.register(ShipmentDelivery)
admin.site.register(ShipmentItem)
admin.site.register(Receivable)
admin.site.register(File)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(OrderUnit)
admin.site.register(SiteSettings)