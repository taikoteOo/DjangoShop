from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from  django.views.generic import (CreateView,
                                   DetailView,
                                   ListView,
                                   UpdateView,
                                   DeleteView)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import CategoryCreateForm, ProductCreateForm, BreweryCreateForm
from .models import Category, Product, Brewery, LikeUser, LikeItem
from cart.views import ProductCartUser


################   АДМИНКА   ################

# Класс для создания категории
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'admin_pages/add_category.html'
    success_url = reverse_lazy('staff:category_add')

# Класс для просмотра категорий
class CategoryListView(ListView):
    model = Category
    template_name = 'admin_pages/list_category.html'
    context_object_name = 'categories'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Сортировка по возрастанию
        queryset = queryset.order_by('pk')
        return queryset

def delete_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    category .delete()
    return redirect('staff:categories')

# Класс для создания пивоварни
class BreweryCreateView(CreateView):
    model = Brewery
    form_class = BreweryCreateForm
    template_name = 'admin_pages/add_brewery.html'
    success_url = reverse_lazy('staff:brewery_add')

# Класс для просмотра пивоварен
class BreweryListView(ListView):
    model = Brewery
    template_name = 'admin_pages/list_brewery.html'
    context_object_name = 'breweries'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Сортировка по возрастанию
        queryset = queryset.order_by('pk')
        return queryset

def delete_brewery(request, slug):
    brewery = get_object_or_404(Brewery, slug=slug)
    brewery .delete()
    return redirect('staff:breweries')

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

    def get_queryset(self):
        queryset = super().get_queryset()
        # Сортировка по возрастанию
        queryset = queryset.order_by('pk')
        return queryset

def delete_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product .delete()
    return redirect('staff:products')

################   Клиентская часть   ################
class ProductsByCategoryListView(ListView):
    model = Product
    template_name = 'shop/beers.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        context['is_products_page'] = True
        # Добавляем текущую категорию, если есть
        slug = self.kwargs.get('slug')
        if slug:
            context['current_category'] = get_object_or_404(Category, slug=slug)

        # Пагинация
        paginator = Paginator(context['products'], 6)  # 6 товаров на странице
        page = self.request.GET.get('page')

        try:
            products_page = paginator.page(page)
        except PageNotAnInteger:
            products_page = paginator.page(1)
        except EmptyPage:
            products_page = paginator.page(paginator.num_pages)

        context['products_page'] = products_page
        return context

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if not slug:
            return Product.objects.all()
        return Product.objects.filter(category__slug=slug)

class ProductDetailClientView(DetailView):
    model = Product
    template_name = 'shop/detail_product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object  # получаем текущий товар
        context['is_products_page'] = True
        if self.request.user.is_authenticated:
            like = ProductLikeUser(self.request)
            cart = ProductCartUser(self.request)
            context['liked'] = product.id in like.like_ids
            context['in_cart'] = product.id in cart.cart_ids
        else:
            context['liked'] = False

        return context

def index(request):
    return render(request, template_name='shop/index.html')


# Класс избранного
class ProductLikeUser:
    def __init__(self, request):
        self.user = request.user
        if not self.user.is_authenticated:
            raise Exception("Избранное доступно только авторизованным пользователям")

        self.like_user, created = LikeUser.objects.get_or_create(user=self.user)
        self.like_ids = list(
            LikeItem.objects.filter(like=self.like_user).values_list('product_id', flat=True)
        )

    def add(self, product):
        product_id = product.id
        if product_id in self.like_ids:
            LikeItem.objects.filter(like=self.like_user, product_id=product_id).delete()
            self.like_ids.remove(product_id)
        else:
            LikeItem.objects.create(like=self.like_user, product=product)
            self.like_ids.append(product_id)

    def remove(self, product_id):
        if product_id in self.like_ids:
            LikeItem.objects.filter(like=self.like_user, product_id=product_id).delete()
            self.like_ids.remove(product_id)

    def get_products(self):
        return Product.objects.filter(id__in=self.like_ids)

    def clear(self):
        LikeItem.objects.filter(like=self.like_user).delete()
        self.like_ids.clear()

    def __len__(self):
        return len(self.like_ids)

    def __iter__(self):
        products = Product.objects.filter(id__in=self.like_ids)
        for product in products:
            yield product

# добавление товара в избранное
def like_add(request, slug):
    product = get_object_or_404(Product, slug=slug)
    # создаем избранное (получаем из сессии или БД)
    like = ProductLikeUser(request)
    like.add(product)
    return redirect('shop:product_detail', slug=slug)

# рендер избранного
def like_detail(request):
    like = ProductLikeUser(request)
    products = like.get_products()

    paginator = Paginator(products, 12)  # 12 товаров на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop/like_detail.html', {'products': page_obj, 'is_profile_page': True})

# удаление товара из избранного
def remove_product_like(request, product_id):
    like = ProductLikeUser(request)
    like.remove(product_id)
    return redirect('shop:like_detail')

# def page_not_found(request, exception):
#     return render(request, template_name='shop/404.html', context={'title':'404'})
#
# def forbidden(request, exception):
#     return render(request, template_name='shop/403.html', context={'title':'403'})
#
# def server_error(request):
#     return render(request, template_name='shop/500.html', context={'title':'500'})

def not_found(request):
    return render(request, template_name='shop/404.html', context={'title': '404'})

def for_bidden(request):
    return render(request, template_name='shop/403.html', context={'title':'403'})

def error_server(request):
    return render(request, template_name='shop/500.html', context={'title':'500'})