"""
URL configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/

Examples
--------
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""

from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import debug
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("backend.apps.crazy_registration.urls")),
    path("auth/", include("rest_framework.urls")),
    path("api/", include("backend.apps.api.urls")),
    path("", RedirectView.as_view(url="/")),
]
# this is for development purpose only
# in production, you should use a reverse proxy like nginx instead
if settings.DEBUG:
    urlpatterns.extend(
        [
            *staticfiles_urlpatterns(),
            path("", debug.default_urlconf),
        ],
    )
