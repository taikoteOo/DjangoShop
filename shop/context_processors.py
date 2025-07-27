from users.forms import RegistrationForm, LoginForm
from cart.views import Cart, ProductCartUser


def register(request):
    return {
        'register': RegistrationForm()
    }

def cart(request):
    if request.user.id:
        return {'cart': ProductCartUser(request)}

    return {'cart': Cart(request)}

def log_in(request):
    return {
        'login': LoginForm()
    }