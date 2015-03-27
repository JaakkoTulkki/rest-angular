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
    permission_classes = (IsAccountOwner,)#(IsAccountOwner, permissions.IsAdminUser)
    authentication_classes = (JSONWebTokenAuthentication, )
    def get_queryset(self):
        return Account.objects.filter(username=self.kwargs.get('username'))

    def update(self, request, username=None):
        user = Account.objects.get(pk=1)
        data = request.data
        pwd = request.data['password']
        data['password'] = pwd
        data['confirm_password'] = pwd
        print('user ', user)
        if user.check_password(pwd) and user.username == username:
            serializer = self.serializer_class(user, data=request.data)
            if serializer.is_valid():
                serializer.update(user, serializer.validated_data)
                user.set_password(pwd)
                user.save()
                update_session_auth_hash(request, user)
                del serializer.validated_data['password']
                del serializer.validated_data['confirm_password']
                return Response(serializer.validated_data, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({
                    'status': "400",
                    'message': 'Your account could not be updated'
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'status': "Authetication failed",
            'message': 'Account could not be updated'
        }, status=status.HTTP_403_FORBIDDEN)


