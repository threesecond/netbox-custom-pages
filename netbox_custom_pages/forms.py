from django import forms
from django.utils.translation import gettext_lazy as _
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import TagFilterField
from utilities.forms.rendering import FieldSet
from django.forms import modelformset_factory
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


class MenuItemForm(forms.ModelForm):
    """
    Inline form for a single page's menu settings.
    Used inside the MenuEditor formset.
    """
    class Meta:
        model = CustomPage
        fields = ('link_text', 'weight', 'is_published')
        widgets = {
            'link_text': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'width:80px;'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# Factory: creates a formset of MenuItemForm for all CustomPage instances
MenuEditorFormSet = modelformset_factory(
    CustomPage,
    form=MenuItemForm,
    extra=0,
)


class CSVImportForm(forms.Form):
    """
    CSV import form for CustomPage metadata.
    Accepts file upload or pasted CSV text.
    Content field is intentionally excluded.
    """
    csv_file = forms.FileField(
        required=False,
        label=_('CSV File'),
        help_text=_('Upload a .csv file. Headers: name, slug, editor_mode, link_text, weight, is_published')
    )
    csv_data = forms.CharField(
        required=False,
        label=_('CSV Data'),
        widget=forms.Textarea(attrs={
            'class': 'form-control font-monospace',
            'rows': 8,
            'placeholder': 'name,slug,editor_mode,link_text,weight,is_published\nMy Page,my-page,html,My Page,100,True'
        }),
        help_text=_('Or paste CSV data directly. File upload takes priority if both are provided.')
    )

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('csv_file') and not cleaned_data.get('csv_data'):
            raise forms.ValidationError(_('Please provide either a CSV file or paste CSV data.'))
        return cleaned_data


class JSONImportForm(forms.Form):
    """
    Form for importing CustomPage objects from a JSON file or pasted JSON text.
    Supports full content import (including HTML content field).
    """
    json_file = forms.FileField(
        required=False,
        label=_('JSON File'),
        help_text=_('Upload a .json file exported from this plugin.')
    )
    json_data = forms.CharField(
        required=False,
        label=_('JSON Data'),
        widget=forms.Textarea(attrs={
            'class': 'form-control font-monospace',
            'rows': 12,
            'placeholder': '[\n  {\n    "name": "My Page",\n    "slug": "my-page",\n    "editor_mode": "html",\n    "content": "<h1>Hello</h1>",\n    "link_text": "My Page",\n    "weight": 100,\n    "is_published": true\n  }\n]'
        }),
        help_text=_('Or paste JSON data directly. File upload takes priority if both are provided.')
    )

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('json_file') and not cleaned_data.get('json_data'):
            raise forms.ValidationError(_('Please provide either a JSON file or paste JSON data.'))
        return cleaned_data