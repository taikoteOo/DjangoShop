from django.urls import path
from .views import ProductsByCategoryListView, ProductDetailClientView, index, like_detail, like_add, remove_product_like


app_name = 'shop'
urlpatterns = [
    path('products/<slug:slug>/info', ProductDetailClientView.as_view(), name='product_detail'),
    path('products/<slug:slug>', ProductsByCategoryListView.as_view(), name='beer_category'),
    path('products/', ProductsByCategoryListView.as_view(), name='beers'),
    path('like/', like_detail, name='like_detail'),
    path('like/add/<slug:slug>/', like_add, name='like_add'),
    path('like/remove/<int:product_id>/', remove_product_like, name='like_remove'),
    path('', index, name='index'),
]