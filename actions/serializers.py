from rest_framework import serializers

from actions.models import Action
from causes.serializers import CauseMemberSerializer

class ActionSerializer(serializers.ModelSerializer):
    cause_member = CauseMemberSerializer()
    class Meta:
        model = Action
        fields = ('cause_member', 'url',)
        read_only_fields = ('created_at', 'updated_at',)

class CreateActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('cause_member', 'url',)
        read_only_fields = ('created_at', 'updated_at',)

    def create(self, validated_data):
        url = validated_data.get('url')
        cause_member = validated_data.get('cause_member')
        return Action.objects.create(url=url, cause_member=cause_member)