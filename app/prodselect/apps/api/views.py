from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import GenericViewSet

from prodselect.apps.api.serializers import ProductSerializer, UserSelectionSerializer, \
    UserSelectionCreateSerializer
from prodselect.apps.products.models import Product
from prodselect.apps.selection.models import Selection


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


class UserSelectionSerializerViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        GenericViewSet,
):
    """
    API endpoint for CRUD operations on selection objects for the current user.

    Same as ModelViewSet but without update functionality - we only want to add or remove
    selection objects.
    """
    queryset = Selection.objects.all()
    serializer_class = UserSelectionSerializer
    create_serializer_class = UserSelectionCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return self.create_serializer_class
        else:
            return self.serializer_class

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
