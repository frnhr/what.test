from rest_framework import viewsets

from prodselect.apps.api.serializers import ProductSerializer
from prodselect.apps.products.models import Product


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing or retrieving products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
