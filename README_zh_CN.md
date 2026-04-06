# NetBox Custom Pages 插件
### 打造专属网页：调用所需 API，随心编辑内容

[English](README.md) | [繁體中文](README_zh_TW.md) | **简体中文**

这是一个功能强大且高度可定制化的 NetBox 插件，允许管理员直接在 NetBox 的用户界面中，创建动态的 HTML/JS 页面与仪表板 (Dashboards)。本插件内置「所见即所得 (WYSIWYG)」编辑器 (Quill.js) 以供撰写简单图文，同时提供「源代码编辑器」 (CodeMirror) 供进阶开发者以 API 驱动的方式开发动态仪表板。

## 功能特色 (Features)
- **双编辑器模式 (Dual Editor Modes)**：可自由切换所见即所得编辑器 (Quill.js) 与纯 HTML/JS 代码编辑器 (CodeMirror)。
- **前台目录大厅 (Public Dashboard Directory)**：一个干净且只读的展示首页，列出所有已发布上线的自定义页面。
- **API 代理支持 (API Proxy Support)**：安全地调用外部 API (如 Grafana, Zabbix)，绝不泄露令牌 (Tokens)。
- **批量管理操作 (Bulk Operations)**：专属的菜单编辑器 (Menu Editor)，可一次调整所有页面的显示设置。
- **导入与导出 (Import/Export)**：完整支持 CSV (Metadata) 与 JSON (完整内容) 的备份与迁移。
- **完整多国语言支持 (Full i18n Support)**：支持多国翻译 (v0.8.0 已内置完整繁/简体中文语言包)。
- **企业级就绪 (Enterprise Ready)**：与 NetBox 4.4+ 版本完美兼容。

---

## 📽️ 操作截图 (Screenshots)

### 1. 打造专属网页：调用所需 API，随心编辑内容
由您亲自定义内容与布局，并能安全地整合系统内外数据源。
![前台首页](docs/img/screenshots-your-own-pages.png)

### 2. 集中化的管理界面
直观、统一的仪表板，让您在一处就能轻松维护所有的自定义页面。
![总览页面](docs/img/screenshots-cuscom-pages.png)

### 3. 菜单与排序权重编辑器
化繁为简的批量编辑体验：一键调整所有链接文字、排序权重与发布状态。
![菜单编辑器](docs/img/screenshots-menu-editor.png)

### 4. 双模式编辑的灵活性
不论是适合快速图文的「富文本 (WYSIWYG)」编辑，或是追求极致控制的「源代码 (HTML/JS)」编辑，通通都能满足。
![富文本编辑器](docs/img/screenshots-wysiwyg-editor.png)
![源代码编辑器](docs/img/screenshots-text-editor.png)

---

## 🔒 安全性与最佳实践

### 1. 敏感信息管理 (通过 Proxy 代理 API)
当您的页面需要整合像是 Grafana 或 Zabbix 的机密数据时，**绝对不可以直接将您的 API Token 写进前端的 HTML/JS 编辑器之中**。
请改将这些具备机密性的访问令牌配置于后台 NetBox 安全的 `configuration.py` 当中：

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

设置好之后，您就可以在自定义页面的 JavaScript 当中，放心地调用插件内置的代理端点 (Proxy Endpoint) 来发送请求：
```javascript
fetch('/api/plugins/custom-pages/proxy/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': document.cookie.split('csrftoken=')[1].split(';')[0]
  },
  body: JSON.stringify({
    target_url: 'https://grafana.internal/api/dashboards',
    token_key: 'grafana_read_only', // 上面对应的 Token 别名
    method: 'GET'
  })
})
```

### 2. 内容安全策略例外 (CSP Exceptions)
默认情况下，NetBox 实施了极为严格的 CSP 规则，这将会阻挡您的 JavaScript 去连接除了 `self` 以外的外部域名。
如果您决定**不使用**內建的 Proxy，并坚持让前端直接跨域获取数据，您必须在 `configuration.py` 手动覆盖加入 `CSP_CONNECT_SRC`：
```python
# configuration.py
CSP_CONNECT_SRC = [
    "'self'", 
    "https://grafana.company.internal", 
    "https://zabbix.company.internal"
]
```

---

## 📦 安装与配置 (Installation)

### 1. 下载并安装
假设您的 NetBox 安装于 `/opt/netbox` 目录下：

```bash
# 克隆源代码
cd /opt
git clone https://github.com/threesecond/netbox-custom-pages.git
cd netbox-custom-pages

# 进入 NetBox 虚拟环境
source /opt/netbox/venv/bin/activate

# 安装插件 (建议使用开发者模式 -e，以便未来 git pull 即可升级)
pip install -e .
```

### 2. 启用插件
编辑您的 `/opt/netbox/netbox/netbox/configuration.py`:

```python
PLUGINS = [
    'netbox_custom_pages',
]

# (选填) 配置 API Proxy 代理金钥
PLUGINS_CONFIG = {
    'netbox_custom_pages': {
        'external_api_keys': {
            'grafana_key': 'Bearer eyJhbGciOiJIUz...',
            'zabbix_auth': 'Api-Token 123456789...'
        },
        'allow_raw_js': True
    }
}
```

### 3. 应用更改并收集静态文件
```bash
cd /opt/netbox/netbox/
python3 manage.py migrate
python3 manage.py collectstatic --no-input
```

### 4. 重启服务
```bash
sudo systemctl restart netbox netbox-rq
```

---

## 🔄 插件升级 (Updating)

若要通过 Git 更新至最新版本：

```bash
cd /opt/netbox-custom-pages
git pull

# 进入环境并应用数据库与静态文件变更
source /opt/netbox/venv/bin/activate
cd /opt/netbox/netbox/
python3 manage.py migrate
python3 manage.py collectstatic --no-input

# 重启服务
sudo systemctl restart netbox netbox-rq
```

---

## 🗑️ 卸载插件 (Uninstallation)

若要从 NetBox 中移除此插件：

1.  **从配置中移除**：编辑 `configuration.py`，将 `'netbox_custom_pages'` 从 `PLUGINS` 列表中移除。
2.  **使用 Pip 卸载**：
    ```bash
    source /opt/netbox/venv/bin/activate
    pip uninstall netbox-custom-pages
    ```
3.  **重启服务**：
    ```bash
    sudo systemctl restart netbox netbox-rq
    ```

> [!IMPORTANT]
> **重要提示：** 卸载插件 **不会** 自动删除数据库中的数据表。如果您希望彻底删除所有数据，您必须手动从数据库中删除名为 `netbox_custom_pages_` 开头的所有数据表。

---

## 🛠️ 兼容性关系表 (Compatibility)

| NetBox 版本     | 插件版本       | 支持状态               |
|----------------|----------------|------------------------|
| 4.4.x - 4.5.x  | 0.8.0+         | ✅ 完全支持 (Supported)|
| 4.3.x          | N/A            | ❌ 不支持 (Unsupported)|
| < 4.2.x        | N/A            | ❌ 不支持 (Unsupported)|

---

## 🤝 支持与社区 (Support)

- **问题回报**: 请至 [GitHub Issues](https://github.com/threesecond/netbox-custom-pages/issues)。
- **讨论区**: 对于一般性问题，请使用 [GitHub Discussions](https://github.com/threesecond/netbox-custom-pages/discussions)。
- **贡献代码**: 我们欢迎 PR！请确保代码通过 CI 测试。
