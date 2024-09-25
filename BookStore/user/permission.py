from rest_framework import permissions

class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        # Kiểm tra xem người dùng đã đăng nhập và có vai trò Admin không
        return request.user.is_authenticated and request.user.role.name == 'Admin'
