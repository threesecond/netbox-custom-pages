from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel

class CustomPage(NetBoxModel):
    """
    儲存自定義頁面的主要模型
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    
    # 儲存 HTML/WYSIWYG 產出的佈局
    content_html = models.TextField(blank=True)
    
    # 儲存使用者寫的 JavaScript 邏輯 (API Call)
    content_js = models.TextField(blank=True)
    
    # 儲存使用者定義的 CSS 樣式
    content_css = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)
        # 這裡會對應到 i18n 的翻譯鍵值
        verbose_name = 'Custom Page'
        verbose_name_plural = 'Custom Pages'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # 這是點擊 NetBox 列表時跳轉到該頁面的連結
        return reverse('plugins:netbox_custom_pages:custompage', args=[self.slug])