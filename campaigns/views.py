from rest_framework import generics

from campaigns.models import Campaign
from campaigns.serializers import CampaignSerializer

class CampaignList(generics.ListAPIView):
    model = Campaign
    serializer_class = CampaignSerializer
    queryset = Campaign.objects.all()