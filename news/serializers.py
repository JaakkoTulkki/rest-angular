from rest_framework import serializers

from news.models import News

class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ('company', 'author', 'title', 'body', 'slug', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'slug')
