from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from companies.models import Company

from kehko.general_permissions import IsCompanyAdmin

from news.models import News
from news.serializers import NewsSerializer

class NewsList(generics.ListCreateAPIView):
    model = News
    serializer_class = NewsSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    queryset = News.objects.all()

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(), )
        else:
            return (IsCompanyAdmin(), )

    def post(self, request, *args, **kwargs):
        obj = Company.objects.get(pk=request.data.get('company', None))
        self.check_object_permissions(request, obj)
        return self.create(request, *args, **kwargs)


