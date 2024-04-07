from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

user_model = get_user_model()


class CrazyAuthenticationForm(AuthenticationForm):
    def clean(self) -> dict:
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        user_model.objects.create_user(username, password)
        # COMPLETELY CRAZY! :)

        return super().clean()
