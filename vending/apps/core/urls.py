from django.contrib import admin
from django.urls import path, include

from vending.apps.core.routers import vending_router
from vending.apps.core.views import TestView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/auth/', include('rest_framework.urls')),

    path('api/v1/auth/', include('vending.apps.vauth.urls')),
    path('api/v1/wallet/', include('vending.apps.wallet.urls')),
    path('api/v1/product/', include('vending.apps.product.urls')),

    path('api/v1/', include(vending_router.urls)),

    path('test', TestView.as_view())
]
