from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

# Notifications group
notifications_items = [
    PluginMenuItem(
        link="plugins:notices:eventnotification_list",
        link_text="Inbound",
        buttons=[
            PluginMenuButton(
                link="plugins:notices:eventnotification_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            )
        ],
    ),
]

# Events group
events_items = [
    PluginMenuItem(
        link="plugins:notices:maintenance_list",
        link_text="Planned Maintenances",
        buttons=[
            PluginMenuButton(
                link="plugins:notices:maintenance_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            )
        ],
    ),
    PluginMenuItem(
        link="plugins:notices:outage_list",
        link_text="Outages",
        buttons=[
            PluginMenuButton(
                link="plugins:notices:outage_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
            )
        ],
    ),
    PluginMenuItem(
        link="plugins:notices:maintenance_calendar",
        link_text="Calendar",
    ),
]

menu = PluginMenu(
    label="Notices",
    groups=(
        ("Notifications", notifications_items),
        ("Events", events_items),
    ),
    icon_class="mdi mdi-wrench",
)
