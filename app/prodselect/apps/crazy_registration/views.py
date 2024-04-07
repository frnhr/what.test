from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from .forms import CrazyAuthenticationForm


class CrazyLoginView(LoginView):
    """CRAZY!!"""

    template_name = "rest_framework/login.html"
    form_class = CrazyAuthenticationForm

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs) -> HttpResponse:
        return super().dispatch(*args, **kwargs)
