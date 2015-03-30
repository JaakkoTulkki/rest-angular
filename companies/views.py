from rest_framework import generics, permissions, status
from rest_framework.response import Response

from rest_framework_jwt.authentication import JSONWebTokenAuthentication


from companies.serializers import CompanySerializer, ProductSerializer
from companies.models import Company, Product

class CompanyList(generics.ListCreateAPIView):
    model = Company
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    authentication_classes = (JSONWebTokenAuthentication, )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(), )
        else:
            return (permissions.IsAdminUser(), )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(account_owner=self.request.user, )
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response({
            'status': "Bad request",
            'message': 'Company could not be created'
        }, status=status.HTTP_400_BAD_REQUEST)

class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Company
    serializer_class = CompanySerializer
    lookup_field = 'slug'
    authentication_classes = (JSONWebTokenAuthentication, )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(), )
        else:
            return (permissions.IsAdminUser(), )

    def get_queryset(self):
        return Company.objects.filter(slug=self.kwargs.get('slug'))

    def update(self, request, *args, **kwargs):
        user = request.user
        queryset = self.get_queryset()[0]
        serializer = CompanySerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(account_owner=user)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({
                'status': "400",
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class ProductList(generics.ListAPIView):
    model = Product
    serializer_class = ProductSerializer
    queryset = Product.objects.all()