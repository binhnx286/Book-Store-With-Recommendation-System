from django.db import models
from django.contrib.auth.models import AbstractUser

# Role
class Role(models.Model):
    name = models.CharField(max_length=255,verbose_name='Vai trò')

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "role"
        verbose_name_plural = 'Phân quyền'

class Account(AbstractUser):
    phone = models.CharField(max_length=255, blank=True, null=True,verbose_name='Số điện thoại')
    address = models.CharField(max_length=255, blank=True, null=True,verbose_name='Địa chỉ')
    status = models.BooleanField(default=True,verbose_name='Trạng thái')  
    role = models.ForeignKey('Role', on_delete=models.CASCADE, related_name="accounts",verbose_name='Vai trò')
    def __str__(self):
        return self.username

    class Meta:
         verbose_name_plural = 'Tài khoản'
#         db_table = "account"

class UserToken(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE,verbose_name='Tài khoản')
    refresh_token = models.TextField()
    access_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Token for {self.user.email} created at {self.created_at}'

    class Meta:
        db_table = "user_token"
        verbose_name_plural = 'Token tài khoản'
        



