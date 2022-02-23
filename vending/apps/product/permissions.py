from rest_framework import permissions


class ProductPermissions(permissions.DjangoObjectPermissions):
    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)

        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_seller
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ['PATCH', 'DELETE', 'PUT']:
            return request.user == obj.seller and request.user.is_seller
        return False


class ProductBuyerPermissions(permissions.DjangoObjectPermissions):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_buyer
        )
