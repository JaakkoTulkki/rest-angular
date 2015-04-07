from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from companies.models import Company
from images.models import Image
from images.serializers import ImageSerializer
from kehko.general_permissions import HasRightsToUploadImage

class ImageList(generics.ListCreateAPIView):
    model = Image
    serializer_class = ImageSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    queryset = Image.objects.all()
    permission_classes = (permissions.AllowAny(), )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(), )
        else:
            return (permissions.IsAuthenticated(), HasRightsToUploadImage(), )

    def create(self, request, *args, **kwargs):
        company_pk =  request.data.get('company', None)
        if company_pk:
            obj = Company.objects.get(pk=company_pk)
        else:
            obj = None
        self.check_object_permissions(request, obj)
        serializer = self.serializer_class(data=request.data, partial=True, context={'uploader': request.user})
        if serializer.is_valid():
            serializer.save(uploader=request.user)
            return Response({'message': "Image uploaded"}, status=status.HTTP_201_CREATED)
        return Response({
            'status': "Bad request",
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)