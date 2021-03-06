
from django.db import DataError, transaction
from django.db.models import F

from rest_framework import parsers, renderers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from vending.apps.product.serializer import BuyProductSerializer
from vending.apps.product.permissions import ProductBuyerPermissions
from vending.apps.product.models import Product
from vending.apps.vauth.models import VendingUser
from vending.apps.wallet.serializers import DepositWalletSerializer


class BuyProductView(APIView):
    """
    Allow user to buy product, receives product as product_id and quantity
    """
    throttle_classes = ()
    permission_classes = (ProductBuyerPermissions, )
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = BuyProductSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def get_change(self, value):
        # returns ([coins], take)
        choices = DepositWalletSerializer.COIN_CHOICES
        to_exchange = value
        change = []
        no_change = 0

        for c in choices:
            while to_exchange / c[0] >= 1:
                change.append(c[0])
                to_exchange -= c[0]
        no_change = to_exchange

        return change, no_change

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        product = Product.objects.get(id=serializer.validated_data['product'])
        quantity = serializer.validated_data['quantity']
        total_spend = product.cost * quantity

        if total_spend > user.deposit:
            return Response({'msg': 'Not enough money.'}, status=status.HTTP_402_PAYMENT_REQUIRED)
        try:
            with transaction.atomic():
                Product.objects.filter(pk=product.pk).update(quantity=F('quantity') - quantity)
                change = user.deposit - total_spend
                VendingUser.objects.filter(pk=user.pk).update(deposit=0)
        except DataError:
            return Response({'msg': 'Could not buy, trt again.'}, status.HTTP_410_GONE)

        user_change, machine_change = self.get_change(change)

        resp = {
            'product': product.name,
            'quantity': quantity,
            'total_spent': total_spend,
            'change': user_change,
            'no-change': machine_change,
            'msg': 'Enjoy your product.'
        }
        return Response(resp)
