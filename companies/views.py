from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({
            'status': "Bad request",
            'message': 'Company could not be created'
        }, status=status.HTTP_400_BAD_REQUEST)

class CompanyDetail(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,
                    generics.GenericAPIView):#generics.RetrieveUpdateDestroyAPIView
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

    def partial_update(self, request, *args, **kwargs):
        queryset = self.get_queryset()[0]
        to_be_removed = self.request.DATA['following_company']
        queryset.following_company.remove(*to_be_removed)
        queryset.save()
        serializer = CompanySerializer(queryset, partial=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class ProductList(generics.ListCreateAPIView):
    model = Product
    serializer_class = ProductSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    lookup_field = 'owner'

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(), )
        else:
            return (permissions.IsAdminUser(), )

    def get_queryset(self):
        return Product.objects.filter(owner__slug=self.kwargs.get('company'))

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            corp = Company.objects.get(slug=kwargs.get('company'))
            serializer.save(owner=corp)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({
            'status': "Bad request",
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Product
    serializer_class = ProductSerializer
    authentication_classes = (JSONWebTokenAuthentication, )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(), )
        else:
            return (permissions.IsAdminUser(), )

    def get_queryset(self):
        return Product.objects.filter(owner__slug=self.kwargs.get('company'), slug=self.kwargs.get('product'))

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset.delete()
        return Response({
            'status': "205",
            'message': "Object deleted"
            }, status=status.HTTP_204_NO_CONTENT
        )

    def update(self, request, *args, **kwargs):
        queryset = self.get_queryset()[0]
        serializer = ProductSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({
                'status': "400",
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)