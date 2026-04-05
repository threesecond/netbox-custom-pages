from django.utils.translation import gettext_lazy as _
from netbox.plugins import PluginMenuItem, PluginMenuButton

# Define the menu items to be injected into the NetBox sidebar
menu_items = (
    PluginMenuItem(
        link='plugins:netbox_custom_pages:custompage_hub',
        link_text=_('Pages Directory'),
        permissions=['netbox_custom_pages.view_custompage'],
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_custom_pages:custompage_list',
                title=_('Manage Pages'),
                icon_class='mdi mdi-cog',
                color='blue',
                permissions=['netbox_custom_pages.add_custompage'],
            ),
            PluginMenuButton(
                link='plugins:netbox_custom_pages:custompage_add',
                title=_('Add Page'),
                icon_class='mdi mdi-plus-thick',
                color='green',
                permissions=['netbox_custom_pages.add_custompage'],
            ),
            PluginMenuButton(
                link='plugins:netbox_custom_pages:menu_editor',
                title=_('Menu Editor'),
                icon_class='mdi mdi-sort',
                color='grey',
                permissions=['netbox_custom_pages.change_custompage'],
            ),
        )
    ),
)