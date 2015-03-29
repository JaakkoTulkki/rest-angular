from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from authentication.serializers import AccountSerializer
from authentication.models import Account
from causes.models import Cause, CauseMembers
from causes.serializers import CauseSerializer, CauseMemberSerializer

class CauseList(generics.ListCreateAPIView):
    model = Cause
    serializer_class = CauseSerializer
    queryset = Cause.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, )

    def get_permissions(self):
        #everybody can see the list of causes
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(), )
        #but only authenticated admins can create causes (at least for now)
        else:
            return (permissions.IsAuthenticated(), permissions.IsAdminUser())

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        serializer = CauseSerializer(data=data, partial=True)
        if serializer.is_valid():
            print('tyyppi ', type(user))
            serializer.save(creator=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({
                    'status': "400",
                    'message': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
