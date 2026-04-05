from netbox.filtersets import NetBoxModelFilterSet
from .models import CustomPage

class CustomPageFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = CustomPage
        fields = ('id', 'name', 'slug', 'editor_mode')
        # Make search field look into name, slug, and content
        search_fields = ('name', 'slug', 'content')
