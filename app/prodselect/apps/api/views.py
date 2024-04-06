from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import GenericViewSet

from prodselect.apps.api.serializers import ProductSerializer, UserSelectionSerializer, \
    UserSelectionCreateSerializer
from prodselect.apps.products.models import Product
from prodselect.apps.selection.models import Selection


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing and retrieving Product objects.
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
    API endpoint for CRUD operations on Selection objects for the current user.

    Mixins: same as ModelViewSet but without update functionality - we only want to add or remove
    Selection objects.
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
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
