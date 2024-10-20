from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


# Role
class Role(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "role"

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Account(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=True)  # Required by Django for custom user models
    role = models.ForeignKey('Role', on_delete=models.CASCADE, related_name="accounts")

    objects = AccountManager()

    USERNAME_FIELD = 'email'  # Use email to log in
    REQUIRED_FIELDS = ['name']  # Fields required when creating a user via createsuperuser

    def __str__(self):
        return self.email

    class Meta:
        db_table = "account"

class UserToken(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    refresh_token = models.TextField()
    access_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Token for {self.user.email} created at {self.created_at}'

    class Meta:
        db_table = "user_token"
        
# ACCOUNT
# class Account(models.Model):
#     name = models.CharField(max_length=255)
#     password = models.CharField(max_length=255)
#     phone = models.CharField(max_length=255, blank=True, null=True)
#     email = models.EmailField(unique=True)
#     address = models.CharField(max_length=255, blank=True, null=True)
#     status = models.BooleanField(default=True)
#     role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="accounts")
    
#     def __str__(self) -> str:
#         return self.email

#     class Meta:
#         db_table = "account"


