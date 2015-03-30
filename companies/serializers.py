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
    account_owner = AccountSerializer()
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
    owner = CompanySerializer()
    class Meta:
        model = Product
        fields = ('owner', 'name', 'slug', 'description', 'price', 'values')

    def create(self, validated_data):
        owner = validated_data['owner']
        name = validated_data['name']
        slug = validated_data['slug']
        description = validated_data['description']
        price = validated_data['price']
        product = Product(owner=owner, name=name, slug=slug, description=description, price=price)
        product.save()
        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance