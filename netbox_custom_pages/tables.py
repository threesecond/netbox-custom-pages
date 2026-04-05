import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from netbox.tables import NetBoxTable, columns
from .models import CustomPage

class CustomPageTable(NetBoxTable):
    """
    Table for displaying CustomPage objects in a list view.
    """
    name = tables.Column(
        linkify=True,
        verbose_name=_('Name')
    )
    editor_mode = tables.Column(
        verbose_name=_('Editor Mode')
    )
    weight = tables.Column(
        verbose_name=_('Weight')
    )
    is_published = columns.BooleanColumn(
        verbose_name=_('Published')
    )
    # Standard NetBox columns for tags and actions (edit/delete)
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = CustomPage
        fields = ('pk', 'id', 'name', 'slug', 'editor_mode', 'weight', 'is_published', 'actions', 'tags')
        default_columns = ('name', 'slug', 'editor_mode', 'weight', 'is_published', 'tags')