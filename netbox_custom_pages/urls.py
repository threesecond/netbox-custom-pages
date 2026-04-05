from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from . import models, views

app_name = 'netbox_custom_pages'

urlpatterns = [
    # Public Dashboard Hub (Entry point)
    path('', views.PublicPageListView.as_view(), name='custompage_hub'),

    # List view for all custom pages
    path('pages/', views.CustomPageListView.as_view(), name='custompage_list'),
    
    # Create a new page
    path('pages/add/', views.CustomPageEditView.as_view(), name='custompage_add'),

    # Menu Editor: bulk-edit display settings for all pages
    path('pages/menu/', views.MenuEditorView.as_view(), name='menu_editor'),
    
    # Detail view in Admin UI
    path('pages/<int:pk>/', views.CustomPageView.as_view(), name='custompage'),
    path('pages/<int:pk>/edit/', views.CustomPageEditView.as_view(), name='custompage_edit'),
    path('pages/<int:pk>/delete/', views.CustomPageDeleteView.as_view(), name='custompage_delete'),
    path('pages/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='custompage_changelog', kwargs={'model': models.CustomPage, 'base_template': 'netbox_custom_pages/custom_page.html'}),

    # Render URL: The actual custom page visible to users
    path('render/<slug:slug>/', views.PageRenderView.as_view(), name='page_render'),
    
    # Documentation Views
    path('docs/css-policy/', views.CSSPolicyView.as_view(), name='css_policy'),
]