from rest_framework import serializers
from authentication.models import Account
from django.contrib.auth import update_session_auth_hash

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'created_at', 'updated_at', 'followees',
                 'first_name', 'last_name', 'tagline', 'password', 'confirm_password', 'date_of_birth',
                  'country', 'liked_products', 'liked_companies', 'liked_causes')
        read_only_fields = ('created_at', 'updated_at')
    def create(self, validated_data):
        print(validated_data)
        return Account.objects.create_user(**validated_data)
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.tagline = validated_data.get('tagline', instance.tagline)
        instance.country = validated_data.get('country', instance.country)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        followees = validated_data.get('followees')
        if followees:
            instance.save()
            instance.followees.add(*followees)
        liked_products = validated_data.get('liked_products')
        if liked_products:
            instance.save()
            instance.liked_products.add(*liked_products)
        liked_companies = validated_data.get('liked_companies')
        if liked_companies:
            instance.save()
            instance.liked_companies.add(*liked_companies)
        liked_causes = validated_data.get('liked_causes')
        if liked_causes:
            instance.save()
            instance.liked_causes.add(*liked_causes)
        instance.save()
        return instance

