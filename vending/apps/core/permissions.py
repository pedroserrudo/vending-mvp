from rest_framework.permissions import BasePermission


class IsBuyerPermission(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_buyer)


class IsSellerPermission(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_seller)
