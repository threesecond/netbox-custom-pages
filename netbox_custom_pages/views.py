from netbox.views import generic
from . import forms, models, tables

class CustomPageListView(generic.ObjectListView):
    """
    View for listing all CustomPage instances.
    """
    queryset = models.CustomPage.objects.all()
    table = tables.CustomPageTable

class CustomPageView(generic.ObjectView):
    """
    View for rendering the actual custom page content.
    """
    queryset = models.CustomPage.objects.all()
    
    def get_template_name(self):
        # We will create this template to render the user's HTML/JS
        return 'netbox_custom_pages/custom_page_render.html'

class CustomPageEditView(generic.ObjectEditView):
    """
    View for creating or editing a CustomPage.
    This is where Monaco and Quill editors will be initialized.
    """
    queryset = models.CustomPage.objects.all()
    form = forms.CustomPageForm
    template_name = 'netbox_custom_pages/custom_page_edit.html'

class CustomPageDeleteView(generic.ObjectDeleteView):
    """
    View for deleting a CustomPage.
    """
    queryset = models.CustomPage.objects.all()
    default_return_url = 'plugins:netbox_custom_pages:custompage_list'