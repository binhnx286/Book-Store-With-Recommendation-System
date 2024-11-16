from rest_framework import viewsets
from .models import Account, Role , UserToken
from .serializers import AccountSerializer , RoleSerializer 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .permission import IsAdminRole
import jwt
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
import random
import string
from .models import Account
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.template.loader import render_to_string

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()  
    serializer_class = AccountSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

class PasswordResetView(APIView):
    def generate_random_password(self, length=32):
        
        characters = string.ascii_letters + string.digits + string.punctuation

        #  ít nhất 1 chữ hoa, 1 chữ thường, 1 số và 1 ký tự đặc biệt
        password = [
            random.choice(string.ascii_uppercase),  
            random.choice(string.ascii_lowercase),  
            random.choice(string.digits),           
            random.choice(string.punctuation),      
        ]
        
        # Điền thêm các ký tự ngẫu nhiên đến đủ độ dài mong muốn
        password += random.choices(characters, k=length-4)  # Đảm bảo độ dài của mật khẩu

        # Trộn mật khẩu để đảm bảo tính ngẫu nhiên
        random.shuffle(password)

        return ''.join(password)

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = Account.objects.filter(email=email).first()
        if not user:
            return Response({"error": "No user found with this email."}, status=status.HTTP_404_NOT_FOUND)
        
        new_password = self.generate_random_password()
        user.password = make_password(new_password)
        user.save()

        html_message = render_to_string(
            'reset_password.html',
            {'email': email, 'new_password': new_password}
        )

        send_mail(
            'Password Reset Notification',
            f'Your new password is: {new_password}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message
        )

        return Response({"message": "A new password has been sent to your email."}, status=status.HTTP_200_OK)



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
                    'user_id': account.pk,
                })
            else:
                return Response({"detail": "Invalid password."}, status=status.HTTP_400_BAD_REQUEST)

        except Account.DoesNotExist:
            return Response({"detail": "Account not found."}, status=status.HTTP_400_BAD_REQUEST)

class ProtectedAPI(APIView):
    permission_classes = [IsAuthenticated]  # Đảm bảo chỉ những người dùng đã xác thực mới truy cập được

    def get(self, request):
        print("User:", request.user)
        print("Is authenticated:", request.user.is_authenticated)

        # Kiểm tra nếu user không phải là Admin
        if request.user.role.name != 'Admin':
            return Response({"error": "Access forbidden. Admins only."}, status=status.HTTP_403_FORBIDDEN)

        # Lấy token từ header
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        
        if auth_header:
            token = auth_header.split(' ')[1]  # Lấy phần token từ Authorization header
            print("Token received:", token)
        else:
            return Response({"error": "No token received"}, status=status.HTTP_401_UNAUTHORIZED)

        # Decode token
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        print("Decoded token:", decoded_token)

        # Trả về thông tin nếu user là Admin
        return Response({
            'user': str(request.user),
            'user_id': request.user.id,
            'decoded_token': decoded_token
        }, status=status.HTTP_200_OK)
