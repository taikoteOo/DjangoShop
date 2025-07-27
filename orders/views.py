import uuid
import json

from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, reverse, render

from .models import Order, OrderItem
from .forms import OrderForm
from cart.views import Cart, ProductCartUser
from cart.models import CartItem
from shop.models import Product


user = get_user_model()


#Создание заказа АНОНИМНЫМ пользователем AJAX запросом
@csrf_exempt
def new_order_ajax(request):
    data = json.loads(request.body)
    name = data.get('name')
    last_name = data.get('lastName')
    email = data.get('email')
    phone = data.get('phone')
    delivery = data.get('delivery')
    payment = data.get('payment')

    cart = Cart(request)
    order = Order.objects.create(name=name,
                         last_name=last_name,
                         email=email,
                         phone=phone,
                         delivery=delivery,
                         payment=payment,
                         number=uuid.uuid4(),
                        )
    for item in cart:
        OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'])

    cart.clear()
    url = reverse("main")
    json_response = {"status": "ok", "url": url}
    return JsonResponse(json_response)


def new_order(request):
    cart = ProductCartUser(request)

    if request.method == "GET":
        order_form = OrderForm()
        return render(request, template_name='orders/order_add.html', context={"form": order_form, "cart": cart})

    if request.method == "POST":
        order_form = OrderForm(request.POST,
                               initial={"number": uuid.uuid4(), "user": request.user, "cart": cart.user_cart})
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.number = uuid.uuid4()
            order.user = request.user
            order.cart = cart.user_cart
            order.name = request.user.username

            order.save()

            for item in cart:
                OrderItem.objects.create(order=order_form.instance, product=item['product'], quantity=item['quantity'])
            cart.user_cart.delete()
        return render(request, template_name='orders/order_create.html', context={"order": order_form.instance})


@login_required
def orders_list(request):
    orders = Order.objects.filter(user=request.user)
    context = {"orders": orders,
               'is_profile_page': True,
               'is_order_change': True,
               }

    return render(request, template_name="orders/orders.html", context=context)


@login_required
def order_detail(request, number):
    order = get_object_or_404(Order, number=number)
    if request.user != order.user:
        raise PermissionDenied
    order_items = order.order_items.all()
    context = {"order": order,
               "order_items": order_items,
               'is_profile_page': True,
               'is_order_change': True,
               }
    return render(request, template_name="orders/order_detail.html", context=context)


def all_orders_list(request):
    admin = user.objects.get(username='staff')
    if request.user != admin:
        raise PermissionDenied

    orders = Order.objects.all()
    context = {"orders": orders}

    return render(request, template_name="shop/admin/orders.html", context=context)

