from django.urls import re_path
from vending.apps.wallet.api_views import DepositWalletView, ResetWalletView, BalanceWalletView


urlpatterns = [

    re_path('deposit/?$', DepositWalletView.as_view()),
    re_path('reset/?$', ResetWalletView.as_view()),
    re_path('balance/?$', BalanceWalletView.as_view())

]
