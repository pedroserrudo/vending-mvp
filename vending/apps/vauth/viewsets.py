# -*- coding: utf-8 -*-
from rest_framework import viewsets

from vending.apps.vauth.models import VendingUser
from vending.apps.vauth.serializers import VendingUserSerializer
from vending.apps.vauth.permissions import VendingUserPermissions


class UserViewSet(viewsets.ModelViewSet):
    queryset = VendingUser.objects.all()
    permission_classes = (VendingUserPermissions,)
    serializer_class = VendingUserSerializer

    def get_queryset(self):
        return super().get_queryset().filter(pk=self.request.user.pk) if self.request.user else None
