from django.views.generic import TemplateView, ListView, View
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
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


class MenuEditorView(PermissionRequiredMixin, View):
    """
    A dedicated interface for bulk-editing menu display settings
    (link_text, weight, is_published) for all custom pages at once.
    """
    permission_required = 'netbox_custom_pages.change_custompage'
    template_name = 'netbox_custom_pages/menu_editor.html'

    def get(self, request):
        queryset = models.CustomPage.objects.all().order_by('weight', 'name')
        formset = forms.MenuEditorFormSet(queryset=queryset)
        return self._render(request, formset, queryset)

    def post(self, request):
        queryset = models.CustomPage.objects.all().order_by('weight', 'name')
        formset = forms.MenuEditorFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Menu settings saved successfully.')
            return redirect('plugins:netbox_custom_pages:menu_editor')
        return self._render(request, formset, queryset)

    def _render(self, request, formset, queryset):
        from django.shortcuts import render
        return render(request, self.template_name, {
            'formset': formset,
            'pages': queryset,
        })