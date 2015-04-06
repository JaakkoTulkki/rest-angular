from django.contrib.auth import update_session_auth_hash
from django.db.models import Q

from itertools import chain

from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from authentication.serializers import AccountSerializer
from authentication.models import Account

from causes.models import Cause
from causes.serializers import CauseSerializer

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
    #queryset = Account.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            #allow only authenticated adminusers
            return (permissions.IsAuthenticated(), permissions.IsAdminUser())
        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

    def get_queryset(self):
        queryset = Account.objects.all()
        ids = self.request.QUERY_PARAMS.get('ids', None)
        if ids:
            ids = ids.split(",")
            ids = [int(id) for id in ids]
            queryset = queryset.filter(pk__in=ids)
        return queryset



    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response({
            'status': "Bad request",
            'message': 'Account could not be created'
        }, status=status.HTTP_400_BAD_REQUEST)



class AccountDetail(generics.RetrieveUpdateAPIView):
    model = Account
    serializer_class = AccountSerializer
    lookup_field = 'username'
    permission_classes = (IsAccountOwner, permissions.IsAuthenticated)
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

class UserCauses(generics.ListAPIView):
    serializer_class = CauseSerializer
    #authentication_classes = (JSONWebTokenAuthentication, )

    def get_permissions(self):
        return (permissions.AllowAny(),)

    def get_queryset(self):
        user = Account.objects.get(username=self.kwargs.get('username'))
        user_query = user.cause_following.all()
        cause_query = Cause.objects.filter(creator=user)
        return list(chain(user_query, cause_query))
