from rest_framework import serializers
from images.models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('uploader', 'company', 'image', 'name')
        read_only_fields = ('uploader', 'company')

    def create(self, validated_data):
        return Image.objects.create(**validated_data)