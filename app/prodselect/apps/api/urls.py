from django.urls import include, path
from rest_framework import routers

from prodselect.apps.api import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'selection', views.UserSelectionSerializerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
