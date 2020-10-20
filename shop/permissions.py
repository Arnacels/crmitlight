from rest_framework import permissions


class PaymasterPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        allow = all((request.user.is_authenticated,
                     request.user.groups.filter(name='Paymaster').exists(),
                     request.data.get('status') == 1))
        return allow


class ShopAssistantPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        allow = all((request.user.is_authenticated,
                     request.user.groups.filter(name='ShopAssistant').exists(),
                     request.data.get('status') == 2))
        return allow


class AccountantPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        allow = all((request.user.is_authenticated, request.user.groups.filter(name='Accountant').exists()))
        return allow
