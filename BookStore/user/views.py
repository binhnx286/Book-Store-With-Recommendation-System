from rest_framework import viewsets
from .models import Account, Role , UserToken
from .serializers import AccountSerializer , RoleSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import check_password
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAdminUser
 


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()  
    serializer_class = AccountSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUser]
    

class AuthToken(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            account = Account.objects.get(email=email)
            
            if check_password(password, account.password):
                # Tạo tokens
                refresh = RefreshToken.for_user(account)
                access_token = refresh.access_token
                access_token['role'] = account.role.name

                # Xóa các token cũ
                UserToken.objects.filter(user=account).delete()

                # Lưu tokens vào cơ sở dữ liệu
                UserToken.objects.create(
                    user=account,
                    refresh_token=str(refresh),
                    access_token=str(access_token),
                )

                return Response({
                    'refresh': str(refresh),
                    'access': str(access_token),
                    'email': account.email,
                    'role': account.role.name, 
                })
            else:
                return Response({"detail": "Invalid password."}, status=status.HTTP_400_BAD_REQUEST)

        except Account.DoesNotExist:
            return Response({"detail": "Account not found."}, status=status.HTTP_400_BAD_REQUEST)