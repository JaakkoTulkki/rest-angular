from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from images.models import Image
from images.serializers import ImageSerializer

class ImageList(generics.ListCreateAPIView):
    model = Image
    serializer_class = ImageSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    queryset = Image.objects.all()
    permission_classes = (permissions.AllowAny(), )

    def get_permissions(self):
        return (permissions.AllowAny(), )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, partial=True, context={'uploader': request.user})
        if serializer.is_valid():
            return Response({'message': "Image uploaded"}, status=status.HTTP_201_CREATED)
        return Response({
            'status': "Bad request",
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)