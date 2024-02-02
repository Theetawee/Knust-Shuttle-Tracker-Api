from rest_framework import generics
from .serializers import AccountSerializer
from .models import Account
# Create your views here.


class UserList(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


users_list=UserList.as_view()