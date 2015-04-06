from rest_framework import serializers
from images.models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('uploader', 'company', 'image')
        read_only_fields = ('uploader', 'company')

    def create(self, validated_data):
        #uploader = validated_data.get('uploader', None)
        #if not uploader:
        #    uploader = self.context.get('uploader', None)
        #print('uploader ', uploader)
        #name = validated_data.get('name', "yo")
        #image = validated_data.get('image')
        #image = Image.objects.create(name=name+str(1), image=image)
        #image.save()
        #return image
        return Image.objects.create(**validated_data)