from rest_framework import generics,permissions, status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from values.serializers import ValueSerializer
from values.models import Value

class ValueList(generics.ListCreateAPIView):
    model = Value
    serializer_class = ValueSerializer
    authentication_classes = (JSONWebTokenAuthentication, )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(), )
        else:
            return (permissions.IsAuthenticated(), )
    def get_queryset(self):
        queryset = Value.objects.all()
        ids = self.request.QUERY_PARAMS.get('ids', None)
        if ids:
            ids = ids.split(",")
            ids = [int(id) for id in ids]
            queryset = queryset.filter(pk__in=ids)
        return queryset

class ValueDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Value
    serializer_class = ValueSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    renderer_classes = (JSONRenderer, )
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        else:
            #only admins able to update or delete
            return (permissions.IsAdminUser(),)

    def get_queryset(self):
        return Value.objects.filter(slug=self.kwargs.get('slug'))
