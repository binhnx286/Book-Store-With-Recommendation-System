from rest_framework import serializers
from .models import Account, Role
from .utils import hash_password


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
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.get("password", None)
        if password:
            hashed_password = hash_password(password)
            validated_data["password"] = hashed_password

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ["id", "name"]
