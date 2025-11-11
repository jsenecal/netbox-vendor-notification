# Navigation Menu Restructure Design

**Date:** 2025-11-11
**Status:** Approved
**Branch:** feature/netbox-notices-refactor

## Overview

Restructure the NetBox Notices plugin navigation menu to better organize notifications and events into logical groups. This improves user workflow by separating inbound notifications from event tracking.

## Current Structure

```
Notices (Plugin Menu)
└─ Notices (Single Group)
   ├─ Maintenance Events
   ├─ Outages
   └─ Calendar
```

**Problems:**
- No access to EventNotification list view (raw vendor emails)
- Single flat group doesn't reflect workflow stages
- No clear distinction between inbound notifications and tracked events

## Proposed Structure

```
Notices (Plugin Menu)
├─ Notifications (Group)
│  └─ Inbound (EventNotifications list + add button)
├─ Events (Group)
│  ├─ Planned Maintenances (Maintenance list + add button)
│  ├─ Outages (Outages list + add button)
│  └─ Calendar (Calendar view - no add button)
```

**Benefits:**
- Clear separation between inbound notifications and event tracking
- EventNotification list view becomes accessible
- Logical workflow: Notifications → Events → Calendar overview
- Future-ready for "Outbound" notifications when implemented

## Implementation Details

### 1. Navigation Menu Updates

**File:** `notices/navigation.py`

Changes:
- Create two menu groups: "Notifications" and "Events"
- Add new menu item for EventNotification list ("Inbound")
- Rename "Maintenance Events" → "Planned Maintenances" for clarity
- Move Calendar into Events group

Menu structure:
```python
notifications_items = [
    PluginMenuItem(
        link="plugins:notices:eventnotification_list",
        link_text="Inbound",
        buttons=[...]
    ),
]

events_items = [
    PluginMenuItem(
        link="plugins:notices:maintenance_list",
        link_text="Planned Maintenances",
        buttons=[...]
    ),
    PluginMenuItem(
        link="plugins:notices:outage_list",
        link_text="Outages",
        buttons=[...]
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
```

### 2. EventNotification ListView

**File:** `notices/views.py`

Add new view class:
```python
class EventNotificationListView(generic.ObjectListView):
    queryset = models.EventNotification.objects.all()
    table = tables.EventNotificationTable
    filterset = filtersets.EventNotificationFilterSet
```

This follows the standard NetBox ObjectListView pattern used by MaintenanceListView and OutageListView.

### 3. EventNotification Table

**File:** `notices/tables.py`

Add new table class:
```python
class EventNotificationTable(NetBoxTable):
    subject = tables.Column(linkify=True)
    email_from = tables.EmailColumn()
    email_received = tables.DateTimeColumn()
    event = tables.Column(
        accessor='event',
        linkify=True,
        verbose_name='Related Event'
    )

    class Meta(NetBoxTable.Meta):
        model = models.EventNotification
        fields = (
            'pk', 'id', 'subject', 'email_from',
            'email_received', 'event', 'actions'
        )
        default_columns = (
            'subject', 'email_from', 'email_received', 'event'
        )
```

Key features:
- Subject links to detail view
- Email column with mailto: link
- Event column links to associated Maintenance/Outage
- Standard NetBox table actions (view, edit, delete)

### 4. URL Routing

**File:** `notices/urls.py`

Add new URL pattern for list view:
```python
path(
    'notifications/',
    views.EventNotificationListView.as_view(),
    name='eventnotification_list'
),
```

Maintains existing patterns:
- `/notifications/` - List view (NEW)
- `/notification/add/` - Add view (existing)
- `/notification/<pk>/` - Detail view (existing)
- `/notification/<pk>/delete/` - Delete view (existing)

### 5. FilterSet

**File:** `notices/filtersets.py`

Add new filterset class:
```python
class EventNotificationFilterSet(NetBoxModelFilterSet):
    email_from = filters.CharFilter(
        lookup_expr='icontains',
        label='From Email'
    )
    email_received = filters.DateFilter()
    email_received__gte = filters.DateFilter(
        field_name='email_received',
        lookup_expr='gte',
        label='Received after'
    )
    email_received__lte = filters.DateFilter(
        field_name='email_received',
        lookup_expr='lte',
        label='Received before'
    )

    class Meta:
        model = models.EventNotification
        fields = ('id', 'subject', 'email_from', 'email_received')
```

Enables filtering by:
- Sender email (contains search)
- Received date (exact, range)
- Subject (search)
- ID (exact)

## Testing Plan

### Manual Testing Checklist

1. **Navigation Menu**
   - [ ] Plugin menu shows two groups: "Notifications" and "Events"
   - [ ] "Inbound" appears under Notifications
   - [ ] "Planned Maintenances", "Outages", "Calendar" appear under Events
   - [ ] All menu items have correct links

2. **EventNotification List View**
   - [ ] Navigate to Notifications → Inbound
   - [ ] List displays existing EventNotifications
   - [ ] Table shows: subject, email_from, email_received, event
   - [ ] Subject links to detail view
   - [ ] Event links to associated Maintenance/Outage
   - [ ] Add button works

3. **Filtering**
   - [ ] Search by email sender works
   - [ ] Date range filtering works
   - [ ] Subject search works

4. **Existing Functionality**
   - [ ] Maintenance Events list still works
   - [ ] Outages list still works
   - [ ] Calendar view still works
   - [ ] All CRUD operations still work

### Automated Testing

Update existing tests:
- `tests/test_navigation.py` - Update menu structure assertions
- `tests/test_url_patterns.py` - Add eventnotification_list URL test
- `tests/test_views.py` - Add EventNotificationListView test
- `tests/test_tables.py` - Add EventNotificationTable test

## Migration Notes

### Database Changes
- None required (no model changes)

### User Impact
- **Breaking Change:** Menu structure changes
- Users must update bookmarks if they bookmarked specific menu items
- No data migration required
- All existing data remains accessible

### Configuration
- No configuration changes required
- No settings updates needed

## Future Enhancements

### Outbound Notifications (Future)
When implementing outbound notification system:
1. Add "Outbound" menu item under Notifications group
2. Create OutboundNotification model
3. Add list view, table, and filterset
4. Link to event dispatching system

### Additional Views (Future)
Consider adding:
- Combined "All Events" view showing both Maintenances and Outages
- Dashboard widget for recent EventNotifications
- Timeline view showing notification → event relationship

## Implementation Checklist

- [ ] Update `notices/navigation.py` with new structure
- [ ] Add `EventNotificationListView` to `notices/views.py`
- [ ] Add `EventNotificationTable` to `notices/tables.py`
- [ ] Add `EventNotificationFilterSet` to `notices/filtersets.py`
- [ ] Add URL pattern to `notices/urls.py`
- [ ] Update tests in `tests/test_navigation.py`
- [ ] Add tests for new components
- [ ] Manual testing verification
- [ ] Update documentation (if applicable)

## References

- NetBox Plugin Development Guide
- Existing plugin structure in netbox-notices
- NetBox generic views documentation
