# NetBox Custom Pages 插件
### 打造專屬網頁：調用所需 API，隨心編輯內容

[English](README.md) | **繁體中文** | [简体中文](README_zh_CN.md)

這是一個功能強大且高度可客製化的 NetBox 外掛程式，允許管理員直接在 NetBox 的使用者介面中，創建動態的 HTML/JS 頁面與儀表板 (Dashboards)。本外掛內建「所見即所得 (WYSIWYG)」編輯器 (Quill.js) 以供撰寫簡單圖文，同時提供「原始碼編輯器」 (CodeMirror) 供進階開發者以 API 驅動的方式開發動態儀表板。

## 功能特色 (Features)
- **雙編輯器模式 (Dual Editor Modes)**：可自由切換所見即所得編輯器 (Quill.js) 與純 HTML/JS 程式碼編輯器 (CodeMirror)。
- **前台目錄大廳 (Public Dashboard Directory)**：一個乾淨且唯讀的展示首頁，列出所有已發布上線的自定義頁面。
- **API 代理支援 (API Proxy Support)**：安全地呼叫外部 API (如 Grafana, Zabbix)，絕不洩露權杖 (Tokens)。
- **批次管理操作 (Bulk Operations)**：專屬的選單編輯器 (Menu Editor)，可一次調整所有頁面的顯示設定。
- **匯入與匯出 (Import/Export)**：完整支援 CSV (Metadata) 與 JSON (完整內容) 的備份與遷移。
- **完整多國語系 (Full i18n Support)**：支援多國翻譯 (v0.8.0 已內建完整繁體中文語系)。
- **企業級就緒 (Enterprise Ready)**：與 NetBox 4.4+ 版本完美相容。

---

## 📽️ 操作截圖 (Screenshots)

### 1. 打造專屬網頁：調用所需 API，隨心編輯內容
由您親自定義內容與佈局，並能安全地整合系統內外數據來源。
![前台首頁](docs/img/screenshots-your-own-pages.png)

### 2. 集中化的管理介面
直覺、統一的儀表板，讓您在一處就能輕鬆維護所有的自定義頁面。
![總覽頁面](docs/img/screenshots-cuscom-pages.png)

### 3. 選單與排序權重編輯器
化繁為簡的批次編輯體驗：一鍵調整所有連結文字、排序權重與發布狀態。
![選單編輯器](docs/img/screenshots-menu-editor.png)

### 4. 雙模式編輯的靈活性
不論是適合快速圖文的「所見即所得編輯器 (WYSIWYG)」編輯，或是追求極致控制的「原始碼 (HTML/JS)」編輯，通通都能滿足。
![富文本編輯器](docs/img/screenshots-wysiwyg-editor.png)
![原始碼編輯器](docs/img/screenshots-text-editor.png)

---

## 🔒 資安防護與最佳實踐

### 1. 敏感資訊管理 (透過 Proxy 代理 API)
當您的頁面需要整合像是 Grafana 或 Zabbix 的機敏資料時，**絕對不可以直接將您的 API Token 寫進前端的 HTML/JS 編輯器之中**。
請改將這些具備機密性的存取權杖配置於後台 NetBox 安全的 `configuration.py` 當中：

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

設定好之後，您就可以在自定義頁面的 JavaScript 當中，安心地呼叫外掛內建的代理端點 (Proxy Endpoint) 來發送請求：
```javascript
fetch('/api/plugins/custom-pages/proxy/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': document.cookie.split('csrftoken=')[1].split(';')[0]
  },
  body: JSON.stringify({
    target_url: 'https://grafana.internal/api/dashboards',
    token_key: 'grafana_read_only', // 上面對應的 Token 別名
    method: 'GET'
  })
})
```

### 2. 內容安全策略例外 (CSP Exceptions)
預設情況下，NetBox 實施了極為嚴格的 CSP 規則，這將會阻擋您的 JavaScript 去連線除了 `self` 以外的外部網域。
如果您決定**不使用**內建的 Proxy，並堅持讓前端直接跨網域取得資料，您必須在 `configuration.py` 手動覆寫加入 `CSP_CONNECT_SRC`：
```python
# configuration.py
CSP_CONNECT_SRC = [
    "'self'", 
    "https://grafana.company.internal", 
    "https://zabbix.company.internal"
]
```

### 3. CSS 污染防範指南
在設計您的自定義網頁樣式時，**絕對不要**使用全域性的 HTML 標籤選擇器（例如：`body { background: black; }`）。
由於您的頁面是被原生地向內坎套至 NetBox 中執行的，這意味著不帶限制的 CSS 標籤將會往外溢出並癱瘓 NetBox 自身的版面排版。請總是透過加上獨立的 Class 來限縮樣式範圍，或是直接善用預載的 Bootstrap 5 類別標籤進行排版。

---

## 系統相容性 (Compatibility)

| NetBox 版本     | 外掛版本       | 支援狀態               |
|----------------|----------------|------------------------|
| 4.4.x - 4.5.x  | 0.8.0+         | ✅ 完全支援 (Supported)|
| 4.3.x          | N/A            | ❌ 不支援 (Unsupported)|
| < 4.2.x        | N/A            | ❌ 不支援 (Unsupported)|

*注意：NetBox 系統會在服務啟動時自動強制執行這些版本邊界限制。如果您在不支援的 NetBox 版本上安裝此外掛，系統將阻擋載入並拋出 `PluginRequirementError`，以保護您的資料庫與系統介面免於毀損。*

---

## 📦 安裝與配置 (Installation)

### 1. 下載並安裝
假設您的 NetBox 安裝於 `/opt/netbox` 目錄下：

```bash
# 複製原始碼
cd /opt
git clone https://github.com/threesecond/netbox-custom-pages.git
cd netbox-custom-pages

# 進入 NetBox 虛擬環境
source /opt/netbox/venv/bin/activate

# 安裝外掛 (建議使用開發者模式 -e，以便未來 git pull 即可升級)
pip install -e .
```

### 2. 啟用外掛
編輯您的 `/opt/netbox/netbox/netbox/configuration.py`:

```python
PLUGINS = [
    'netbox_custom_pages',
]

# (選填) 配置 API Proxy 代理金鑰
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

### 3. 套用變更並收集靜態檔案
```bash
cd /opt/netbox/netbox/
python3 manage.py migrate
python3 manage.py collectstatic --no-input
```

### 4. 重新啟動服務
```bash
sudo systemctl restart netbox netbox-rq
```

---

## 🔄 外掛升級 (Updating)

若要透過 Git 更新至最新版本：

```bash
cd /opt/netbox-custom-pages
git pull

# 進入環境並套用資料庫與靜態檔案變更
source /opt/netbox/venv/bin/activate
cd /opt/netbox/netbox/
python3 manage.py migrate
python3 manage.py collectstatic --no-input

# 重新啟動服務
sudo systemctl restart netbox netbox-rq
```

---

## 🗑️ 移除外掛 (Uninstallation)

若要從 NetBox 中移除此外掛：

1.  **從配置中移除**：編輯 `configuration.py`，將 `'netbox_custom_pages'` 從 `PLUGINS` 列表中移除。
2.  **使用 Pip 解除安裝**：
    ```bash
    source /opt/netbox/venv/bin/activate
    pip uninstall netbox-custom-pages
    ```
3.  **重新啟動服務**：
    ```bash
    sudo systemctl restart netbox netbox-rq
    ```

> [!IMPORTANT]
> **重要提示：** 解除安裝外掛 **不會** 自動刪除資料庫中的資料表。如果您希望徹底刪除所有資料，您必須手動從資料庫中刪除名為 `netbox_custom_pages_` 開頭的所有資料表。

---
