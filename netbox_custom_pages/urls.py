from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from . import models, views

app_name = 'netbox_custom_pages'

urlpatterns = [
    # List view for all custom pages
    path('pages/', views.CustomPageListView.as_view(), name='custompage_list'),
    
    # Create a new page
    path('pages/add/', views.CustomPageEditView.as_view(), name='custompage_add'),
    
    # Individual page view (The actual custom content)
    path('pages/<slug:slug>/', views.CustomPageView.as_view(), name='custompage'),
    
    # Edit/Delete/ChangeLog views (Standard NetBox operations)
    path('pages/<slug:slug>/edit/', views.CustomPageEditView.as_view(), name='custompage_edit'),
    path('pages/<slug:slug>/delete/', views.CustomPageDeleteView.as_view(), name='custompage_delete'),
    path('pages/<slug:slug>/changelog/', ObjectChangeLogView.as_view(), name='custompage_changelog', kwargs={'model': models.CustomPage}),
    
]