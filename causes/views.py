from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from authentication.serializers import AccountSerializer
from authentication.models import Account
from causes.models import Cause, CauseMembers
from causes.serializers import CauseSerializer, CauseMemberSerializer
from kehko.general_permissions import IsAccountOwner

class CauseList(generics.ListCreateAPIView):
    model = Cause
    serializer_class = CauseSerializer
    authentication_classes = (JSONWebTokenAuthentication, )

    def get_permissions(self):
        #everybody can see the list of causes
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(), )
        #but only authenticated admins can create causes (at least for now)
        else:
            return (permissions.IsAuthenticated(), permissions.IsAdminUser())

    def get_queryset(self):
        queryset = Cause.objects.all()
        ids = self.request.QUERY_PARAMS.get('ids', None)
        if ids:
            ids = ids.split(",")
            ids = [int(id) for id in ids]
            queryset = queryset.filter(pk__in=ids)
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        serializer = CauseSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save(creator=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({
                    'status': "400",
                    'message': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

class CauseDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Cause
    serializer_class = CauseSerializer
    lookup_field = 'slug'
    authentication_classes = (JSONWebTokenAuthentication, )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(), )
        else:
            return (permissions.IsAdminUser(), )

    def get_queryset(self):
        return Cause.objects.filter(slug=self.kwargs.get('slug'))

    def update(self, request, *args, **kwargs):
        user = request.user
        queryset = self.get_queryset()[0]
        serializer = CauseSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(creator=user)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({
                'status': "400",
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class CauseMemberCreate(generics.ListCreateAPIView):
    model = CauseMembers
    serializer_class = CauseMemberSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = CauseMembers.objects.all()
        ids = self.request.QUERY_PARAMS.get('ids', None)
        if ids:
            ids = ids.split(",")
            ids = [int(id) for id in ids]
            queryset = queryset.filter(pk__in=ids)
        return queryset

class CauseMemberUpdate(generics.RetrieveUpdateAPIView):
    model = CauseMembers
    serializer_class = CauseMemberSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    queryset = CauseMembers.objects.all()
