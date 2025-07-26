from django.urls import path
from .views import (CategoryCreateView, CategoryListView, ProductCreateView, ProductListView, ProdictDetailView,
                    delete_category, delete_product, delete_brewery, BreweryCreateView, BreweryListView)


app_name = 'staff'
urlpatterns = [
    path('categories/add/', CategoryCreateView.as_view(), name='category_add'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('delete/<slug:slug>/', delete_category, name='category_delete'),

    path('breweries/add/', BreweryCreateView.as_view(), name='brewery_add'),
    path('breweries/', BreweryListView.as_view(), name='breweries'),
    path('delete/<slug:slug>/', delete_brewery, name='brewery_delete'),

    path('products/add/', ProductCreateView.as_view(), name='product_add'),
    path('products/<slug:slug>/', ProdictDetailView.as_view(), name='product_detail'),
    path('products/', ProductListView.as_view(), name='products'),
    path('delete/<slug:slug>/', delete_product, name='product_delete'),
]