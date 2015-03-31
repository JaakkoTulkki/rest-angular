from rest_framework import serializers
from causes.models import Cause, CauseMembers

from authentication.models import Account
from authentication.serializers import AccountSerializer
from companies.serializers import CompanySerializer, ProductSerializer
from values.serializers import ValueSerializer

class CauseMemberSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, required=False)
    class Meta:
        model = CauseMembers
        fields = ('company', 'cause', 'products')

class CauseSerializer(serializers.ModelSerializer):
    creator = AccountSerializer()
    sponsors = CompanySerializer(many=True, required=False)
    values = ValueSerializer(many=True, required=False)
    followers = AccountSerializer(many=True, required=False)
    members = CauseMemberSerializer(many=True, required=False)
    class Meta:
        model = Cause
        fields = ('creator', 'name', 'slug', 'description','sponsors', 'values',
                  'followers', 'members',)
        read_only_fields = ('slug',)

    def create(self, validated_data):
        creator = validated_data['creator']
        name = validated_data['name']
        description = validated_data['description']
        cause = Cause(creator=creator, name=name, description=description)
        cause.save()
        return cause

    def update(self, instance, validated_data):
        instance.creator = validated_data.get('creator', instance.creator)
        instance.sponsors = validated_data.get('sponsors', instance.sponsors)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance