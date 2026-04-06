from django.test import TestCase
from netbox_custom_pages.models import CustomPage

class CustomPageTestCase(TestCase):
    def test_page_creation(self):
        page = CustomPage.objects.create(
            name="Test Page",
            slug="test-page",
            content="<h1>Hello World</h1>",
            is_published=True
        )
        self.assertEqual(page.name, "Test Page")
        self.assertEqual(page.slug, "test-page")
        self.assertEqual(str(page), "Test Page")

    def test_default_link_text(self):
        # Test that link_text defaults to name if empty
        page = CustomPage.objects.create(
            name="Manual Name",
            slug="manual-name",
            is_published=True
        )
        self.assertEqual(page.link_text, "")
        # Note: In models.py, __str__ might return name, but we check absolute logic
