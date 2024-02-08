from django.urls import path
from .views import (
    homepage_view,
    message_us_view,
    place_order_view,
)

app_name = 'website'


urlpatterns = [
    path('', homepage_view, name='home'),
    path('message-us/', message_us_view, name='message_us'),
    path('order/', place_order_view, name='place-order'),
]
