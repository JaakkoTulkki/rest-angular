from rest_framework import serializers
from companies.models import Company, Product
from authentication.serializers import AccountSerializer

from values.serializers import ValueSerializer

"""
class FollowCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'full_name')
"""
class CompanySerializer(serializers.ModelSerializer):
    values = ValueSerializer(many=True, required=False)
    following_company = serializers.HyperlinkedRelatedField(many=True,
                                                            view_name='company-detail',
                                                            queryset=Company.objects.all())
    following_user = AccountSerializer(many=True)
    class Meta:
        model = Company
        fields = ('account_owner', 'full_name', 'slug', 'following_company', 'following_user',
                  'following_campaign', 'likes', 'values')

    def create(self, validated_data):
        account_owner = validated_data['account_owner']
        full_name = validated_data['full_name']
        slug = validated_data['slug']
        company = Company(account_owner=account_owner, full_name=full_name, slug=slug,)
        company.save()
        return company

    def update(self, instance, validated_data):
        instance.account_owner = validated_data.get('account_owner', instance.account_owner)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    values = ValueSerializer(many=True, required=False)
    class Meta:
        model = Product
        fields = ('owner', 'name', 'slug', 'description', 'price', 'values')