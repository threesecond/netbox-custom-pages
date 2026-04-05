from django.views.generic import TemplateView, ListView
from netbox.views import generic
from . import forms, models, tables, filtersets

class CustomPageListView(generic.ObjectListView):
    """
    View for listing all CustomPage instances.
    """
    queryset = models.CustomPage.objects.all()
    table = tables.CustomPageTable
    filterset = filtersets.CustomPageFilterSet
    filterset_form = forms.CustomPageFilterForm

class CustomPageView(generic.ObjectView):
    """
    Standard Detail View for Admin UI
    """
    queryset = models.CustomPage.objects.all()
    template_name = 'netbox_custom_pages/custom_page.html'

class CustomPageEditView(generic.ObjectEditView):
    """
    View for creating or editing a CustomPage.
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

class PageRenderView(generic.ObjectView):
    """
    View for rendering the actual custom page content.
    """
    queryset = models.CustomPage.objects.all()
    template_name = 'netbox_custom_pages/page_render.html'

    def get_object(self, **kwargs):
        # Get by slug
        return self.queryset.get(slug=self.kwargs['slug'])

class CSSPolicyView(TemplateView):
    """
    View for serving the static CSS Documentation with i18n
    """
    template_name = 'netbox_custom_pages/docs/css_policy.html'

class PublicPageListView(ListView):
    """
    Public dashboard hub that lists available custom pages.
    """
    model = models.CustomPage
    template_name = 'netbox_custom_pages/public_index.html'
    context_object_name = 'pages'

    def get_queryset(self):
        # Only show published pages, ordered by weight
        return super().get_queryset().filter(is_published=True).order_by('weight', 'name')