from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from  django.views.generic import (CreateView,
                                   DetailView,
                                   ListView,
                                   UpdateView,
                                   DeleteView)
from .forms import CategoryCreateForm, ProductCreateForm
from .models import Category, Product


################   АДМИНКА   ################

# Класс для создания категории
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'admin_pages/add_category.html'
    success_url = reverse_lazy('staff:categories')

# Класс для просмотра категорий
class CategoryListView(ListView):
    model = Category
    template_name = 'admin_pages/list_category.html'
    context_object_name = 'categories'

# Класс для создания товара
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'admin_pages/add_product.html'
    success_url = reverse_lazy('staff:products')

# Класс для отображения товара
class ProductListView(ListView):
    model = Product
    template_name = 'admin_pages/list_product.html'
    context_object_name = 'products'

# Класс для отображения информации о товаре
class ProdictDetailView(DetailView):
    model = Product
    template_name = 'admin_pages/detail_product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

################   Клиентская часть   ################

class ProductsByCategoryListView(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        return context

    def get_queryset(self):
        # Если не выбрана категория, возврщает все товары
        if not self.kwargs.get('slug'):
            return Product.objects.all()
        # Получаем название категории из URL
        # и возвращаем товары выбранной категории
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Product.objects.filter(category=category)

class ProductDetailClientView(DetailView):
    model = Product
    template_name = 'shop/detail_product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'