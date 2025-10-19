from rest_framework import serializers
from hirethon_template.users.models import Organization

class OrganizationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'slug']
