from netbox.plugins import PluginMenuItem

# Define the menu items to be injected into the NetBox sidebar
menu_items = (
    PluginMenuItem(
        link='plugins:netbox_custom_pages:custompage_list',
        link_text='Custom Pages',
        permissions=['netbox_custom_pages.view_custompage'],
    ),
)