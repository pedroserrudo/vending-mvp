from django.db.models import F

from rest_framework import parsers, renderers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from vending.apps.core.permissions import IsBuyerPermission, IsSellerPermission
from vending.apps.vauth.models import VendingUser
from vending.apps.wallet.serializers import DepositWalletSerializer


class DepositWalletView(APIView):
    throttle_classes = ()
    permission_classes = (IsBuyerPermission, )
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = DepositWalletSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        coins = serializer.validated_data['coins']
        VendingUser.objects.filter(pk=request.user.pk).update(deposit=F('deposit')+sum(coins))
        user = VendingUser.objects.get(pk=request.user.pk)
        return Response({'msg': 'Coins added to your wallet.', 'balance': user.deposit})


class ResetWalletView(APIView):
    throttle_classes = ()
    permission_classes = (IsBuyerPermission, )
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def get(self, request, format=None):
        VendingUser.objects.filter(pk=request.user.pk).update(deposit=0)
        user = VendingUser.objects.get(pk=request.user.pk)
        return Response({'msg': 'Wallet reset.', 'balance': user.deposit})


class BalanceWalletView(APIView):
    throttle_classes = ()
    permission_classes = (IsBuyerPermission, )
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def get(self, request, format=None):

        return Response({'msg': 'Available balance {}'.format(request.user.deposit), 'balance': request.user.deposit})
