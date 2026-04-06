from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from netbox_custom_pages.models import CustomPage

class CustomPageViewTestCase(TestCase):
    def setUp(self):
        # Create a user with necessary permissions
        self.user = User.objects.create_user(username='test-user', password='password')
        
        # Grant permissions for CustomPage
        content_type = ContentType.objects.get_for_model(CustomPage)
        permissions = Permission.objects.filter(content_type=content_type)
        self.user.user_permissions.add(*permissions)
        
        self.client = Client()
        self.client.login(username='test-user', password='password')
        
        # Create a test page
        self.page = CustomPage.objects.create(
            name="Sample Page",
            slug="sample-page",
            content="<p>Test content</p>",
            is_published=True
        )

    def test_list_view(self):
        url = reverse('plugins:netbox_custom_pages:custompage_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Page")

    def test_render_view(self):
        # The public render view
        url = reverse('plugins:netbox_custom_pages:page_render', kwargs={'slug': 'sample-page'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test content")

    def test_menu_editor_view(self):
        url = reverse('plugins:netbox_custom_pages:menu_editor')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Menu Editor")
