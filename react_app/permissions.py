from rest_framework.permissions import BasePermission
import random


class MyPermission(BasePermission):
    message = {
        "status": False,
        "error": "You do not have permission to perform this action."
    }

    def has_permission(self, request, view):
        num = random.randint(1, 10)
        if num % 2 == 0:
            return True
        else:
            return False
