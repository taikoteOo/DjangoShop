from django.urls import path
from .views import ProductsByCategoryListView, ProductDetailClientView, index


app_name = 'shop'
urlpatterns = [
    path('products/<slug:slug>/info', ProductDetailClientView.as_view(), name='product_detail'),
    path('products/<slug:slug>', ProductsByCategoryListView.as_view(), name='beer_category'),
    path('products/', ProductsByCategoryListView.as_view(), name='beers'),
    path('', index, name='index'),
]