from rest_framework import permissions


class VendingUserPermissions(permissions.DjangoObjectPermissions):
    def has_permission(self, request, view):

        if request.method in ['POST', 'HEAD', 'OPTIONS']:
            return True

        return bool(
                request.user and
                request.user.is_authenticated
            )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and
            request.user.is_authenticated and
            obj == request.user
        )
