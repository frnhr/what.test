"""
Makes every login attempt with an unknown email valid, by creating a new user
with that email and password. Crazy!

Even MORE CRAZY: if the user already exists, it will update the password with
the new one.

It's just for a test task ;)


Include this before DRF url patterns.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.CrazyLoginView.as_view(), name="login"),
]
