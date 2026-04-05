from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from netbox_custom_pages.models import CustomPage

class CustomPageSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_custom_pages-api:custompage-detail'
    )

    class Meta:
        model = CustomPage
        fields = (
            'id', 'url', 'display', 'name', 'slug', 'content', 'editor_mode', 
            'tags', 'custom_fields', 'created', 'last_updated',
        )
