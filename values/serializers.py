from rest_framework import serializers
from values.models import Value

class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = ('name', 'description', 'likes', 'created_at', 'updated_at')