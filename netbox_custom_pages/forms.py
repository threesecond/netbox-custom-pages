from django import forms
from django.utils.translation import gettext_lazy as _
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import TagFilterField
from utilities.forms.rendering import FieldSet
from .models import CustomPage

class CustomPageForm(NetBoxModelForm):
    """
    Form for creating and editing CustomPage instances.
    """
    fieldsets = (
        FieldSet('name', 'slug', 'editor_mode', 'tags', name=_('Page Identification')),
        FieldSet('link_text', 'weight', 'is_published', name=_('Directory Settings')),
        FieldSet('content', name=_('Content')),
    )

    class Meta:
        model = CustomPage
        fields = ('name', 'slug', 'editor_mode', 'link_text', 'weight', 'is_published', 'content', 'tags')
        
        # Hidden input mapped to our JavaScript editors in the template
        widgets = {
            'content': forms.Textarea(attrs={'id': 'id_content_sync', 'style': 'display: none;'}),
        }

class CustomPageFilterForm(NetBoxModelFilterSetForm):
    model = CustomPage
    
    editor_mode = forms.ChoiceField(
        choices=CustomPage.EDITOR_CHOICES,
        required=False,
        label=_('Editor Mode')
    )