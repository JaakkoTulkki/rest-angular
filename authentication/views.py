from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from authentication.serializers import AccountSerializer
from authentication.models import Account

class AccountList(generics.ListCreateAPIView):
    model = Account
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            #allow only authenticated user
            return (permissions.AllowAny(),)
        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            print('tulee validated data')
            print(serializer.validated_data)
            Account.objects.create_user(**serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response({
            'status': "Bad request",
            'message': 'Account could not be created'
        }, status=status.HTTP_400_BAD_REQUEST)

class AccountDetail(generics.RetrieveUpdateAPIView):
    model = Account
    serializer_class = AccountSerializer
    lookup_field = 'username'
    #permission_classes = (permissions.IsAdminUser,)
    authentication_classes = (JSONWebTokenAuthentication, )
    def get_queryset(self):
        print(self.request.user)
        return Account.objects.filter(username=self.kwargs.get('username'))
