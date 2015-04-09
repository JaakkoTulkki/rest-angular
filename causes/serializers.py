from rest_framework import serializers
from causes.models import Cause, CauseMembers

from authentication.models import Account
from authentication.serializers import AccountSerializer
from values.serializers import ValueSerializer


class CauseMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CauseMembers
        fields = ('id', 'company', 'cause', 'products', 'mission_statement', 'cause_name')
        read_only_fields = ('id', )

    def update(self, instance, validated_data):
        products = validated_data.get('products')
        if products:
            instance.save()
            instance.products.add(*products)
        instance.save()
        return instance

class CauseSerializer(serializers.ModelSerializer):
    creator = AccountSerializer()
    members = CauseMemberSerializer(many=True, required=False)
    class Meta:
        model = Cause
        fields = ('id', 'creator', 'name', 'slug', 'description','sponsors', 'values',
                  'followers', 'members',)
        read_only_fields = ('slug',)

    def create(self, validated_data):
        creator = validated_data['creator']
        name = validated_data['name']
        description = validated_data['description']
        cause = Cause(creator=creator, name=name, description=description)
        values = validated_data.get('values', [])
        cause.save()
        cause.values.add(*values)
        cause.save()
        return cause

    def update(self, instance, validated_data):
        instance.creator = validated_data.get('creator', instance.creator)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        sponsors = validated_data.get('sponsors')
        if sponsors:
            instance.save()
            instance.sponsors.add(*sponsors)
        followers = validated_data.get('followers')
        if followers:
            instance.save()
            instance.followers.add(*followers)
        instance.save()
        return instance