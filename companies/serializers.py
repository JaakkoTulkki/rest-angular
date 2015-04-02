from rest_framework import serializers
from companies.models import Company, Product
from authentication.serializers import AccountSerializer

from values.serializers import ValueSerializer

class CompanySerializer(serializers.ModelSerializer):
    values = ValueSerializer(many=True, required=False)
    #following_user = AccountSerializer(many=True)
    #account_owner = AccountSerializer()
    class Meta:
        model = Company
        fields = ('id', 'account_owner', 'company_name', 'slug', 'following_company', 'following_user',
                  'following_cause', 'likes', 'values')
        read_only_fields = ('slug', )

    def create(self, validated_data):
        account_owner = validated_data.get('account_owner')
        company_name = validated_data.get('company_name')
        company = Company(account_owner=account_owner, company_name=company_name)
        company.save()
        return company

    def update(self, instance, validated_data):
        instance.account_owner = validated_data.get('account_owner', instance.account_owner)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        following_company = validated_data.get('following_company')
        if following_company:
            instance.save()
            instance.following_company.add(*following_company)
        following_user = validated_data.get('following_user')
        if following_user:
            instance.save()
            instance.following_user.add(*following_user)
        following_cause = validated_data.get('following_cause')
        if following_cause:
            instance.save()
            instance.following_cause.add(*following_cause)
        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    values = ValueSerializer(many=True, required=False)
    owner = CompanySerializer()
    class Meta:
        model = Product
        fields = ('owner', 'name', 'slug', 'description', 'price', 'values')
        read_only_fields = ('slug', )

    def create(self, validated_data):
        owner = validated_data['owner']
        name = validated_data['name']
        description = validated_data['description']
        price = validated_data['price']
        product = Product(owner=owner, name=name, description=description, price=price)
        product.save()
        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance