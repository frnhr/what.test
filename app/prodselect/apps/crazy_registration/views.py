from django.contrib.auth.views import LoginView


from .forms import CrazyAuthenticationForm


class CrazyLoginView(LoginView):
    """CRAZY!!"""

    template_name = 'rest_framework/login.html'
    form_class = CrazyAuthenticationForm
