from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import MethodNotAllowed
from todos.models import Todo


class TodoPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return True

            if request.method in SAFE_METHODS or request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
                return True

            else:
                raise MethodNotAllowed(request.method)

        return False
        