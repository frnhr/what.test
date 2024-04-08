from typing import ClassVar

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from backend.apps.products.models import Product
from backend.apps.selection.models import Selection

user_model = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields: ClassVar = ["id", "name", "price", "stock", "description"]


class UserSelectionSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Selection
        fields: ClassVar = ["url", "id", "product"]


class UserSelectionCreateSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer only for creating a new Selection object."""

    product_id = serializers.UUIDField()
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Selection
        fields: ClassVar = ["product_id", "product"]

    def validate(self, attrs: dict) -> dict:
        attrs = super().validate(attrs)
        self._validate_unique_for_user(attrs)
        return attrs

    def _validate_unique_for_user(self, attrs: dict) -> None:
        user = self.context["request"].user
        if user.selections.filter(product_id=attrs["product_id"]).exists():
            raise ValidationError(_("This product is already selected."))

    def create(self, validated_data: dict) -> Selection:
        user = self.context["request"].user
        product_id = validated_data["product_id"]
        selection = Selection.objects.create(user=user, product_id=product_id)
        return selection


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields: ClassVar = ["email"]
