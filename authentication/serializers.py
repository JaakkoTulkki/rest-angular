from rest_framework import serializers
from authentication.models import Account
from django.contrib.auth import update_session_auth_hash

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    first_name = serializers.CharField(required=False, allow_null=True)
    last_name = serializers.CharField(required=False, allow_null=True)
    tagline = serializers.CharField(required=False, allow_null=True)
    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'created_at', 'updated_at',
                 'first_name', 'last_name', 'tagline', 'password', 'confirm_password')
        read_only_fields = ('created_at', 'updated_at')
    def create(self, validated_data):
        return Account.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.tagline = validated_data.get('tagline', instance.tagline)
        instance.save()
        return instance

