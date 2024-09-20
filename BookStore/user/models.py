from django.db import models


# Role
class Role(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "role"


# ACCOUNT
class Account(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="accounts")
    
    def __str__(self) -> str:
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
