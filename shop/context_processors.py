from users.forms import RegistrationForm


def register(request):
    return {
        'register': RegistrationForm()
    }
