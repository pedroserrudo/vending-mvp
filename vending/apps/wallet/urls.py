from django.urls import path
from vending.apps.wallet.api_views import DepositWalletView, ResetWalletView, BalanceWalletView


urlpatterns = [

    path('deposit', DepositWalletView.as_view()),
    path('reset', ResetWalletView.as_view()),
    path('balance', BalanceWalletView.as_view())

]
