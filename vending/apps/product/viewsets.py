from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from vending.apps.product.models import Product
from vending.apps.product.serializer import ProductSerializer
from vending.apps.product.permissions import ProductPermissions


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated, ProductPermissions)
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
