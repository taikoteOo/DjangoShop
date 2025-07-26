from django.urls import path
from .views import new_order_ajax, new_order, orders_list, order_detail


app_name = 'orders'
urlpatterns = [
    path('new/quick/', new_order_ajax, name='new_quick_order'),  # Anonym USER - AJAX
    path('new/', new_order, name='new_order'),
    path('list/', orders_list, name='orders'),
    path('detail/<str:number>/', order_detail, name='order_detail'),
]