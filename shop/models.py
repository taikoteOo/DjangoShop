from django.db import models
from django.urls import reverse
from slugify import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        pass
        # return reverse('shop:category_detail', kwargs={'slug': self.slug})

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание товара', blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    image = models.ImageField(upload_to='products', blank=True, null=True,verbose_name='Изображение')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    available = models.BooleanField(default=True, verbose_name='Доступность')
    created_ad = models.DateTimeField(auto_now_add=True, editable=False)
    update = models.DateTimeField(auto_now=True, editable=False)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='Категория товара')

    class Meta:
        ordering = ['category','name']
        indexes= [
            models.Index(fields=['id']),
            models.Index(fields=['name']),
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        slug_nane = slugify(self.name)
        slug = f'{slug_nane}-{self.pk}'
        self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('staff:product_detail', kwargs={'slug': self.slug})