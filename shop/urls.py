from django.urls import path
from .views import (ProductsByCategoryListView, ProductDetailClientView, index,
                    like_detail, like_add, remove_product_like,
                    not_found, for_bidden, error_server)


app_name = 'shop'
urlpatterns = [
    path('products/<slug:slug>/info', ProductDetailClientView.as_view(), name='product_detail'),
    path('products/<slug:slug>', ProductsByCategoryListView.as_view(), name='beer_category'),
    path('products/', ProductsByCategoryListView.as_view(), name='beers'),
    path('like/', like_detail, name='like_detail'),
    path('like/add/<slug:slug>/', like_add, name='like_add'),
    path('like/remove/<int:product_id>/', remove_product_like, name='like_remove'),
    path('', index, name='index'),

    path('404', not_found, name='404'),
    path('403', for_bidden, name='403'),
    path('500', error_server, name='500'),
]