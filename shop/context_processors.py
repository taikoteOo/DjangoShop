from users.forms import RegistrationForm
from cart.views import Cart, ProductCartUser


def register(request):
    return {
        'register': RegistrationForm()
    }

def cart(request):
    if request.user.id:
        return {'cart': ProductCartUser(request)}

    return {'cart': Cart(request)}