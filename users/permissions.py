from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied, NotFound
from users.models import UserToken


class HasValidToken(BasePermission):
    def has_permission(self, request, view):
        token_string = view.kwargs.get('token')
        if not token_string:
            raise PermissionDenied("Token not provided")

        try:
            token_obj = UserToken.objects.get(token=token_string)
        except UserToken.DoesNotExist:
            raise NotFound("Token not found")

        if not token_obj.is_valid():
            raise PermissionDenied("Token is expired or inactive")

        # прикріплюємо токен до request для подальшого використання
        request.token_obj = token_obj
        return True
