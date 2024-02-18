from django.urls import path
from .views import (
    store_home_view,
    product_detail_view,
    cart_view,
    checkout_view,
    login_view,
    signup_view,
)


app_name = 'store'


urlpatterns = [
    path('', store_home_view, name="home"),
    path('signup/', signup_view, name="signup"),
    path('login/', login_view, name="login"),
    path('checkout/', checkout_view, name="checkout"),
    path('cart/', cart_view, name="cart"),
    path('<item_id>/', product_detail_view, name="product"),

]
