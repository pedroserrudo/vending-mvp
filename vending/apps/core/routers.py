# -*- coding: utf-8 -*-
from rest_framework import routers

from vending.apps.vauth.viewsets import UserViewSet
from vending.apps.product.viewsets import ProductViewSet

vending_router = routers.DefaultRouter()

vending_router.register(r'users', UserViewSet)
vending_router.register(r'product', ProductViewSet)
