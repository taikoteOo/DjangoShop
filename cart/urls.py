from django.urls import path
from .views import (cart_detail, update_cart_by_front, remove_product,
                    remove_cart, get_cart_length, remove_product_ajax, cart_add)


app_name = 'cart'
urlpatterns = [
    path('detail/', cart_detail, name='cart_detail'),
    path('add/<slug:slug>/', cart_add, name='cart_add'),
    path('update_cart_session/', update_cart_by_front, name="update_cart_session"),
    path('remove_fetch/', remove_product_ajax, name="remove_product_ajax"),
    path('remove/<int:product_id>/', remove_product, name='remove_product'),
    path('clear/', remove_cart, name='remove_cart'),
]