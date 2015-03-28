from django.contrib.auth import update_session_auth_hash

from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from authentication.serializers import AccountSerializer
from authentication.models import Account


from kehko.general_permissions import IsAccountOwner
class RestrictedView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    def get(self, request):
        #print(request.META['Authorization'])
        data = {
        'id': request.user.id,
        'username': request.user.username,
        'token': str(request.auth)
        }
        return Response(data)


class AccountList(generics.ListCreateAPIView):
    model = Account
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            #allow only authenticated user
            return (IsAccountOwner(), permissions.IsAdminUser(), )
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
    permission_classes = (IsAccountOwner, permissions.IsAuthenticated) #(permissions.AllowAny,)
    authentication_classes = (JSONWebTokenAuthentication, )
    def get_queryset(self):
        return Account.objects.filter(username=self.kwargs.get('username'))

    def update(self, request, username=None):
        obj = Account.objects.get(username=username)
        self.check_object_permissions(request, obj)
        user = request.user
        data = request.data
        pwd = request.data.get('password', '')
        if user.check_password(pwd) and request.user == obj:
            serializer = self.serializer_class(user, data=data, partial=True)
            if serializer.is_valid():
                serializer.update(user, serializer.validated_data)
                user_obj = self.serializer_class(user)
                return Response(user_obj.data, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({
                    'status': "400",
                    'message': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'status': "Authentication failed",
            'message': 'Account could not be updated'
        }, status=status.HTTP_403_FORBIDDEN)


