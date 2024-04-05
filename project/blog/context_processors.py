from .forms import LoginFrom, RegistrationForm


def add_my_forms(request):
    return {
        'login_form': LoginFrom(),
        'register_form': RegistrationForm()
    }
