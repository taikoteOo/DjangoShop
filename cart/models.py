from django.db import models
from django.contrib.auth import get_user_model
from shop.models import Product


User = get_user_model()

# Сама корзина
class CartUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

# Элемент корзины
class CartItem(models.Model):
    cart = models.ForeignKey(CartUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']