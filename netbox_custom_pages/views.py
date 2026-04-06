from django.views.generic import TemplateView, ListView, View
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse
from netbox.views import generic
from . import forms, models, tables, filtersets
import json

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
        return render(request, self.template_name, {
            'formset': formset,
            'pages': queryset,
        })


class CustomPageImportView(generic.ObjectImportView):
    """
    Standard NetBox CSV import view for CustomPage metadata.
    Content field is intentionally excluded from CSV import.
    """
    queryset = models.CustomPage.objects.all()
    model_form = forms.CustomPageImportForm


class JSONImportView(PermissionRequiredMixin, View):
    """
    Import CustomPage objects (including HTML content) from a JSON file or text.
    Existing slugs are skipped to prevent accidental overwrites.
    """
    permission_required = 'netbox_custom_pages.add_custompage'
    template_name = 'netbox_custom_pages/json_import.html'

    def get(self, request):
        form = forms.JSONImportForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.JSONImportForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        # Parse JSON - file takes priority over textarea
        try:
            if request.FILES.get('json_file'):
                raw = request.FILES['json_file'].read().decode('utf-8')
            else:
                raw = form.cleaned_data['json_data']
            data = json.loads(raw)
            if not isinstance(data, list):
                raise ValueError('Root element must be a JSON array.')
        except (json.JSONDecodeError, ValueError) as e:
            form.add_error(None, f'Invalid JSON: {e}')
            return render(request, self.template_name, {'form': form})

        # Process each record
        created, skipped, errors = [], [], []
        allowed_fields = {'name', 'slug', 'editor_mode', 'content', 'link_text', 'weight', 'is_published'}

        for i, record in enumerate(data, start=1):
            slug = record.get('slug', '')
            if not slug:
                errors.append(f'Record #{i}: missing required field "slug".')
                continue
            if models.CustomPage.objects.filter(slug=slug).exists():
                skipped.append(slug)
                continue
            try:
                obj = models.CustomPage(**{k: v for k, v in record.items() if k in allowed_fields})
                obj.full_clean()
                obj.save()
                created.append(slug)
            except Exception as e:
                errors.append(f'Record #{i} ({slug}): {e}')

        return render(request, self.template_name, {
            'form': forms.JSONImportForm(),
            'result': {'created': created, 'skipped': skipped, 'errors': errors},
        })


class JSONExportView(PermissionRequiredMixin, View):
    """
    Export all CustomPage objects (including HTML content) as a downloadable JSON file.
    """
    permission_required = 'netbox_custom_pages.view_custompage'

    def get(self, request):
        pages = models.CustomPage.objects.all().order_by('weight', 'name')
        data = [
            {
                'name': p.name,
                'slug': p.slug,
                'editor_mode': p.editor_mode,
                'content': p.content,
                'link_text': p.link_text,
                'weight': p.weight,
                'is_published': p.is_published,
            }
            for p in pages
        ]
        response = HttpResponse(
            json.dumps(data, ensure_ascii=False, indent=2),
            content_type='application/json'
        )
        response['Content-Disposition'] = 'attachment; filename="netbox_custom_pages_export.json"'
        return response