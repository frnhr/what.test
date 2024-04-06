from rest_framework import serializers

from prodselect.apps.products.models import Product
from prodselect.apps.selection.models import Selection


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock', 'description']


class UserSelectionSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Selection
        fields = ["url", "id", "product"]


class UserSelectionCreateSerializer(serializers.HyperlinkedModelSerializer):
    product = serializers.UUIDField()

    class Meta:
        model = Selection
        fields = ["product"]

    def create(self, validated_data):
        user = self.context["request"].user
        product_id = validated_data["product"]
        selection = Selection.objects.create(user=user, product_id=product_id)
        return selection
