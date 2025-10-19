from rest_framework import serializers
from .models import ShortURL

class ShortURLCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ['id', 'original_url', 'slug', 'created_at', 'clicks']
        read_only_fields = ['id', 'slug', 'created_at', 'clicks']