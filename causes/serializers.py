from rest_framework import serializers
from causes.models import Cause, CauseMembers

from authentication.serializers import AccountSerializer
from companies.serializers import CompanySerializer, ProductSerializer
from values.serializers import ValueSerializer

class CauseMemberSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    class Meta:
        model = CauseMembers
        fields = ('company', 'cause', 'products')

class CauseSerializer(serializers.ModelSerializer):
    sponsors = CompanySerializer(many=True)
    values = ValueSerializer(many=True)
    followers = AccountSerializer(many=True)
    members = CauseMemberSerializer(many=True)
    class Meta:
        model = Cause
        fields = ('creator', 'name', 'sponsors', 'slug', 'description', 'likes', 'followers', 'members')

