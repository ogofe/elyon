from django.urls import path
from .views import (
    store_home_view,
    product_detail_view,
    cart_view,
)


app_name = 'store'


urlpatterns = [
    path('', store_home_view, name="home"),
    path('cart/', cart_view, name="cart"),
    path('<item_id>/', product_detail_view, name="product"),

]
