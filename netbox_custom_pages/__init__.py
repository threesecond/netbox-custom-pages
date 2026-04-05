from netbox.plugins import PluginConfig

class NetBoxCustomPagesConfig(PluginConfig):
    name = 'netbox_custom_pages'
    verbose_name = 'NetBox Custom Pages'
    description = 'Create custom web pages within NetBox using HTML and JS'
    version = '0.5.0'
    author = 'Samuel Lin'
    min_version = '4.4.0'
    max_version = '4.5.99'
    base_url = 'custom-pages'
    
    # Default plugin settings for third-party API configurations
    default_settings = {
        'external_api_keys': {},
        'allow_raw_js': True,
    }

config = NetBoxCustomPagesConfig