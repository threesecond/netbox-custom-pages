from netbox.api.routers import NetBoxRouter
from django.urls import path
from . import views

app_name = 'netbox_custom_pages'

router = NetBoxRouter()
router.register('custom-pages', views.CustomPageViewSet)

urlpatterns = router.urls + [
    path('proxy/', views.ExternalAPIProxyView.as_view(), name='api-proxy'),
]
