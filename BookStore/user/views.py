from rest_framework import viewsets
from .models import Account, Role
from .serializers import AccountSerializer , RoleSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()  
    serializer_class = AccountSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer