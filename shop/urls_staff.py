from django.urls import path
from .views import CategoryCreateView, CategoryListView, ProductCreateView, ProductListView, ProdictDetailView


app_name = 'staff'
urlpatterns = [
    path('categories/add/', CategoryCreateView.as_view(), name='category_add'),
    path('categories/', CategoryListView.as_view(), name='categories'),

    path('products/add/', ProductCreateView.as_view(), name='product_add'),
    path('products/<slug:slug>/', ProdictDetailView.as_view(), name='product_detail'),
    path('products/', ProductListView.as_view(), name='products'),
]