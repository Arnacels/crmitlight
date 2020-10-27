from rest_framework import permissions


class ShopStaffPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        allow_paymaster = all((request.user.is_authenticated,
                               request.user.groups.filter(name='Paymaster').exists(),
                               any((request.data.get('status') == 1, request.data.get('status') == 3))))
        allow_shop_assistant = all((request.user.is_authenticated,
                                    request.user.groups.filter(name='ShopAssistant').exists(),
                                    request.data.get('status') == 2))
        return any((allow_shop_assistant, allow_paymaster))


class AccountantPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allow = all((request.user.is_authenticated, request.user.groups.filter(name='Accountant').exists()))
        print(allow)
        return allow
