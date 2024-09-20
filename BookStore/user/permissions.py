from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        token = request.headers.get('Authorization')

        if token:
            try:
                token = token.split(' ')[1]
                try:
                    access_token = AccessToken(token)
                    print(f"Decoded token: {access_token}")
                except Exception as e:
                    print(f"Error decoding token: {e}")

                user_id = access_token.payload.get('user_id')
                
                # Kiểm tra xem người dùng có tồn tại không
                User = get_user_model()
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    print("User not found in the database.")
                    return False

                # Kiểm tra vai trò
                role_name = access_token.payload.get('role')
                return role_name == 'Admin'
            except Exception as e:
                print(f"Error decoding token: {e}")
                return False
        
        return False
