from netbox.api.viewsets import NetBoxModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.conf import settings
from netbox_custom_pages.models import CustomPage
from .serializers import CustomPageSerializer

class CustomPageViewSet(NetBoxModelViewSet):
    queryset = CustomPage.objects.all()
    serializer_class = CustomPageSerializer

class ExternalAPIProxyView(APIView):
    """
    Proxy endpoint to securely fetch data from external APIs using tokens stored in configuration.py.
    This hides tokens from the frontend and solves cross-origin restrictions.
    """
    def post(self, request, *args, **kwargs):
        target_url = request.data.get('target_url')
        token_key = request.data.get('token_key')
        method = request.data.get('method', 'GET').upper()
        payload = request.data.get('payload', None)
        
        if not target_url:
            return Response({'error': 'target_url is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Get plugin settings
        plugin_settings = settings.PLUGINS_CONFIG.get('netbox_custom_pages', {})
        api_keys = plugin_settings.get('external_api_keys', {})
        
        headers = {'Content-Type': 'application/json'}
        
        # Attach token if requested and exists in config
        if token_key:
            token_value = api_keys.get(token_key)
            if not token_value:
                return Response(
                    {'error': f'Token key "{token_key}" not found in NetBox PLUGINS_CONFIG'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            headers['Authorization'] = str(token_value)
            
        try:
            if method == 'GET':
                response = requests.get(target_url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(target_url, headers=headers, json=payload, timeout=10)
            elif method == 'PUT':
                response = requests.put(target_url, headers=headers, json=payload, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(target_url, headers=headers, timeout=10)
            else:
                return Response({'error': f'Method {method} not supported'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
                
            response.raise_for_status()
            
            # Try parsing JSON, fallback to raw text
            try:
                data = response.json()
            except ValueError:
                data = response.text
                
            return Response({'data': data, 'status': response.status_code})
            
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_502_BAD_GATEWAY)
