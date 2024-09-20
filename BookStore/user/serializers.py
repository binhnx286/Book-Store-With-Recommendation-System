from rest_framework import serializers
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Account, Role
from .utils import hash_password, check_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class AccountSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model = Account
        fields = [
            "id",
            "name",
            "password",
            "phone",
            "email",
            "address",
            "status",
            "role",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        hashed_password = hash_password(password)
        validated_data["password"] = hashed_password
        account = super().create(validated_data)

        if account:
            # Render mail content
            html_message = render_to_string('email.html', {'email': account.email})

            # Send email
            send_mail(
                'New Account Created',
                f'An account has been created for {account.email}.',
                settings.DEFAULT_FROM_EMAIL,
                [account.email],  
                fail_silently=False,
                html_message=html_message  
            )

        return account

    def update(self, instance, validated_data):
        password = validated_data.get("password", None)
        if password:
            hashed_password = hash_password(password)
            validated_data["password"] = hashed_password

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, account):
        token = super().get_token(account)
        # Thêm các thông tin khác như user_id hoặc email
        token['user_id'] = account.id
        token['email'] = account.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['email'] = self.user.email
        return data
    
class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ["id", "name"]
