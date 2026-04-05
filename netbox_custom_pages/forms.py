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