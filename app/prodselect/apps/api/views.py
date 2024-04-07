from __future__ import annotations

from typing import ClassVar

from django.db.models import QuerySet
from rest_framework import mixins, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import RetrieveAPIView
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import GenericViewSet

from prodselect.apps.api.serializers import (
    ProductSerializer,
    UserSelectionCreateSerializer,
    UserSelectionSerializer,
    UserSerializer,
)
from prodselect.apps.products.models import Product
from prodselect.apps.selection.models import Selection
from prodselect.apps.users.models import User


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for listing and retrieving Product objects."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends: ClassVar = [SearchFilter, OrderingFilter]
    search_fields: ClassVar = ["name"]
    ordering_fields: ClassVar = ["name", "price", "stock"]
    ordering: ClassVar = ["name"]


class UserSelectionSerializerViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    API endpoint for CRUD operations on Selection objects for the current user.

    Mixins: same as ModelViewSet but without update functionality - we only want
    to add or remove Selection objects.
    """

    queryset = Selection.objects.all()
    serializer_class = UserSelectionSerializer
    create_serializer_class = UserSelectionCreateSerializer

    def get_serializer_class(self) -> type[ModelSerializer]:
        if self.action == "create":
            return self.create_serializer_class
        else:
            return self.serializer_class

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class MeView(RetrieveAPIView):
    """API endpoint for retrieving the current user's data."""

    serializer_class = UserSerializer

    def get_object(self) -> User:
        return self.request.user
