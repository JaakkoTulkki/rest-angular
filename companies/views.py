from rest_framework import generics, status
from rest_framework.response import Response

from companies.serializers import CompanySerializer, ProductSerializer
from companies.models import Company, Product

class CompanyList(generics.ListCreateAPIView):
    model = Company
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

class ProductList(generics.ListAPIView):
    model = Product
    serializer_class = ProductSerializer
    queryset = Product.objects.all()