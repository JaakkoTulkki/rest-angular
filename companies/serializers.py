from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from companies.models import Company, Product
from authentication.serializers import AccountSerializer

from values.serializers import ValueSerializer

class CompanySerializer(serializers.ModelSerializer):
    values = ValueSerializer(many=True, required=False)
    class Meta:
        model = Company
        fields = ('id', 'account_owner', 'company_name', 'slug', 'following_company', 'following_user',
                  'following_cause', 'likes', 'values', 'about', 'founded', 'country', 'description',
                  'mission')
        read_only_fields = ('slug', )

    def create(self, validated_data):
        account_owner = validated_data.get('account_owner')
        company_name = validated_data.get('company_name')
        founded = validated_data.get('founded')
        country = validated_data.get('country')
        about = validated_data.get('about')
        description = validated_data.get('description')
        company = Company(account_owner=account_owner, company_name=company_name)
        company.founded = founded
        company.country = country
        company.about = about
        company.description = description
        company.save()
        return company

    def update(self, instance, validated_data):
        instance.account_owner = validated_data.get('account_owner', instance.account_owner)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.founded = validated_data.get('founded', instance.founded)
        instance.country = validated_data.get('country', instance.country)
        instance.about = validated_data.get('about', instance.about)
        instance.description = validated_data.get('description', instance.description)
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
    owner = CompanySerializer(required=True)

    class Meta:
        #https://github.com/tomchristie/django-rest-framework/issues/2380
        #The model serializer here is generating a UniqueTogetherValidator
        #for Company's account_owner and Product's name
        # due to some nested problems it is not validating correctly
        #Thus we have to overwrite is and check for uniqueness in validate method
        validators = []
        model = Product
        fields = ('owner', 'name', 'slug', 'description', 'price', 'values')
        read_only_fields = ('slug', )

    def validate(self, attrs):
        if self.context.get('method') == 'POST':
            corp = Company.objects.get(slug=self.context.get('corp'))
            #check for uniqueness between product name and product owner
            p = Product.objects.filter(owner=corp, name=attrs['name'])
            if p.exists():
                msg = 'Custom error: violating unique_together("name", "owner") . ' \
                      'Change the name of your product or update your current products'
                raise serializers.ValidationError(msg)
        return attrs

    def create(self, validated_data):
        owner = validated_data.get('owner')
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