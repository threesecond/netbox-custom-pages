<p align="center">
  <img src="netbox_custom_pages/static/netbox_custom_pages/img/icon.png" width="128" height="128" alt="NetBox Custom Pages Icon">
</p>

# NetBox Custom Pages Plugin
### Creating custom web pages made easy!

**English** | [繁體中文](README_zh_TW.md)

A powerful, highly-customizable NetBox plugin allowing administrators to create dynamic HTML/JS pages and dashboards right from the NetBox UI. It features a built-in WYSIWYG editor (Quill.js) for simple text pages, and a raw HTML/JS Code Editor (CodeMirror) for advanced API-driven dashboards.

## Features
- **Dual Editor Modes**: Choose between a Rich Text Editor (Quill.js) and a Raw HTML/JS Editor (CodeMirror).
- **Public Dashboard Directory**: A clean, read-only index page displaying all published custom pages.
- **API Proxy Support**: Securely call external APIs (Grafana, Zabbix) without leaking tokens.
- **Bulk Operations**: Dedicated Menu Editor for bulk updating display settings.
- **Import/Export**: Full support for CSV (Metadata) and JSON (Full Content) backup and portability.
- **Full i18n Support**: Ready for translation into multiple languages (v0.8.0+ includes pre-translated Traditional Chinese).
- **Enterprise Ready**: Seamlessly compatible with NetBox 4.4+.

---

## 📽️ Screenshots
![Manage Pages](file:///C:/Users/threesecond/.gemini/antigravity/brain/c437f470-9337-4a13-8ec1-60337af94cb4/media__1775434381486.png)

---

## 🛠️ Dependencies

- **NetBox**: 4.4.0+
- **Python**: 3.10+
- **Django**: 5.0+ (bundled with NetBox)

## 🔒 Security & Best Practices

### 1. Secrets Management (Proxy API)
When integrating with external systems like Grafana or Zabbix, **NEVER code your API tokens directly into the HTML/JS Editor.** 
Instead, configure your tokens securely in NetBox's `configuration.py`:

```python
PLUGINS_CONFIG = {
    'netbox_custom_pages': {
        'external_api_keys': {
            'grafana_read_only': 'Bearer eyJhbGciOiJIUz...',
            'zabbix_auth': 'Api-Token 123456789...'
        }
    }
}
```

Then, in your Custom Page JavaScript, use the built-in Plugin Proxy Endpoint:
```javascript
fetch('/api/plugins/custom-pages/proxy/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': document.cookie.split('csrftoken=')[1].split(';')[0]
  },
  body: JSON.stringify({
    target_url: 'https://grafana.internal/api/dashboards',
    token_key: 'grafana_read_only', // Matches the alias mapped above
    method: 'GET'
  })
})
```

### 2. Content Security Policy (CSP) Exceptions
By default, NetBox enforces strict CSP rules that block your JavaScript from connecting to external domains. 
If you choose NOT to use the Proxy Proxy and must fetch directly from an external domain, you must update the `CSP_CONNECT_SRC` in your `configuration.py`:
```python
# configuration.py
CSP_CONNECT_SRC = [
    "'self'", 
    "https://grafana.company.internal", 
    "https://zabbix.company.internal"
]
```

### 3. CSS Pollution Guidelines
When styling your custom pages, do **not** use global CSS selectors (e.g., `body { background: black; }`). Your custom pages are embedded natively into NetBox, meaning global tags will overwrite the primary NetBox layout. Always use scoped wrapper classes or default Bootstrap 5 utility classes.

---

## Compatibility Matrix

| NetBox Version | Plugin Version | Status             |
|----------------|----------------|--------------------|
| 4.4.x - 4.5.x  | 0.8.0+         | ✅ Fully Supported |
| 4.3.x          | N/A            | ❌ Not Supported   |
| < 4.2.x        | N/A            | ❌ Not Supported   |

*Note: NetBox programmatically enforces these boundaries during startup. A `PluginRequirementError` will be raised if you attempt to install this plugin on an unsupported NetBox version to prevent database or UI corruption.*

---

## Installation 
*(Standard NetBox Plugin installation procedure...)*

1. Add `netbox_custom_pages` to `PLUGINS` in `configuration.py`.
2. Run database migrations: `python manage.py makemigrations netbox_custom_pages` then `python manage.py migrate`.
3. Restart the NetBox WSGI service.

---

## 🤝 Support & Community

- **Bug Reports**: Please open an issue on [GitHub Issues](https://github.com/threesecond/netbox-custom-pages/issues).
- **Discussions**: For general questions, use [GitHub Discussions](https://github.com/threesecond/netbox-custom-pages/discussions).
- **Contributing**: We welcome pull requests! Please ensure all code passes the CI linting and tests.
