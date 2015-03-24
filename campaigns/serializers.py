from rest_framework import serializers
from campaigns.models import Campaign, CampaignMembers

from authentication.serializers import AccountSerializer
from companies.serializers import CompanySerializer, ProductSerializer
from values.serializers import ValueSerializer

class CampaignMemberSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    class Meta:
        model = CampaignMembers
        fields = ('company', 'campaign', 'products')

class CampaignSerializer(serializers.ModelSerializer):
    sponsors = CompanySerializer(many=True)
    values = ValueSerializer(many=True)
    followers = AccountSerializer(many=True)
    members = CampaignMemberSerializer(many=True)
    class Meta:
        model = Campaign
        fields = ('creator', 'name', 'sponsors', 'slug', 'description', 'likes', 'followers', 'members')

