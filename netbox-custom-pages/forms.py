from django import forms
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import TagFilterField
from .models import CustomPage

class CustomPageForm(NetBoxModelForm):
    """
    Form for creating and editing CustomPage instances.
    """
    # Use fieldsets to organize the layout in NetBox UI
    fieldsets = (
        ('Page Identification', ('name', 'slug', 'tags')),
        ('Content Editors', ('content_html', 'content_js', 'content_css')),
    )

    class Meta:
        model = CustomPage
        fields = ('name', 'slug', 'content_html', 'content_js', 'content_css', 'tags')
        
        # We use HiddenInput or specific widgets because 
        # JavaScript (Quill/Monaco) will take over these textareas.
        widgets = {
            'content_html': forms.Textarea(attrs={'class': 'hidden', 'id': 'id_content_html'}),
            'content_js': forms.Textarea(attrs={'class': 'hidden', 'id': 'id_content_js'}),
            'content_css': forms.Textarea(attrs={'class': 'hidden', 'id': 'id_content_css'}),
        }