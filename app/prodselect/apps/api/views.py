from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from prodselect.apps.api.serializers import ProductSerializer
from prodselect.apps.products.models import Product


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing or retrieving products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'price', 'stock']
    ordering = ['name']
