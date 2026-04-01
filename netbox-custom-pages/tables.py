import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from .models import CustomPage

class CustomPageTable(NetBoxTable):
    """
    Table for displaying CustomPage objects in a list view.
    """
    name = tables.Column(
        linkify=True
    )
    # Standard NetBox columns for tags and actions (edit/delete)
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = CustomPage
        fields = ('pk', 'id', 'name', 'slug', 'actions', 'tags')
        default_columns = ('name', 'slug', 'tags')