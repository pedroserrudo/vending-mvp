from django.urls import path

from vending.apps.product.api_views import BuyProductView


urlpatterns = [
    path('buy', BuyProductView.as_view()),
]
