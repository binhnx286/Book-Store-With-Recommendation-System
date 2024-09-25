from django.contrib import admin
from .models import Role , Account , UserToken
# Register your models here.
admin.site.register(Role)
admin.site.register(Account)
admin.site.register(UserToken)
