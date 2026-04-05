from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from netbox.models import NetBoxModel

class CustomPage(NetBoxModel):
    """
    Main model to store custom web pages created by users.
    """
    EDITOR_CHOICES = (
        ('wysiwyg', _('WYSIWYG Editor')),
        ('html', _('Raw HTML Editor')),
    )

    name = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name=_("Page Name")
    )
    slug = models.SlugField(
        max_length=100, 
        unique=True,
        help_text=_("Unique URL-friendly identifier (e.g., 'my-status-page')")
    )
    content = models.TextField(
        blank=True,
        verbose_name=_("Content")
    )
    editor_mode = models.CharField(
        max_length=20,
        choices=EDITOR_CHOICES,
        default='wysiwyg',
        verbose_name=_("Editor Mode")
    )
    link_text = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Menu Link Text"),
        help_text=_("Optional text to display in the directory menu. Defaults to Name if blank.")
    )
    weight = models.PositiveSmallIntegerField(
        default=100,
        verbose_name=_("Weight / Order"),
        help_text=_("Display order in the directory (lower numbers appear first).")
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name=_("Published"),
        help_text=_("If unchecked, this page will be hidden from the public directory.")
    )

    class Meta:
        ordering = ('weight', 'name',)
        verbose_name = _('Custom Page')
        verbose_name_plural = _('Custom Pages')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Links the model to the detail view
        return reverse('plugins:netbox_custom_pages:custompage', args=[self.pk])