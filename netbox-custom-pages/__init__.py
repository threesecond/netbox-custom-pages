from netbox.plugins import PluginConfig

class NetBoxCustomPagesConfig(PluginConfig):
    name = 'netbox_custom_pages'
    verbose_name = 'NetBox Custom Pages'
    description = 'Create custom web pages within NetBox using HTML and JS'
    version = '0.1.0'
    author = 'Your Name'
    base_url = 'custom-pages'
    
    # 預留第三方 API 的配置空間
    default_settings = {
        'external_api_keys': {},
        'allow_raw_js': True,
    }

config = NetBoxCustomPagesConfig