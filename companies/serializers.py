from rest_framework import serializers
from companies.models import Company, Product
from authentication.serializers import AccountSerializer

from values.serializers import ValueSerializer

class FollowCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'full_name')

class CompanySerializer(serializers.ModelSerializer):
    values = ValueSerializer(many=True)
    following_company = FollowCompanySerializer(many=True)
    following_user = AccountSerializer(many=True)
    class Meta:
        model = Company
        fields = ('account_owner', 'full_name', 'slug', 'following_company', 'following_user', 'likes', 'values')


class ProductSerializer(serializers.ModelSerializer):
    values = ValueSerializer(many=True)
    class Meta:
        model = Product
        fields = ('owner', 'name', 'slug', 'description', 'price', 'values')