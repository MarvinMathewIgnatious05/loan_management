from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Custom permission to allow only Admin users to access a view.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == "Admin"
