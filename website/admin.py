from django.contrib import admin
from .models import Visitor, CarouselItem, Message, SiteVisit


# Register your models here.
admin.site.register(Visitor)
admin.site.register(SiteVisit)
admin.site.register(Message)
admin.site.register(CarouselItem)