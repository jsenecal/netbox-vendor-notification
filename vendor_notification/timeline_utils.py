"""
Timeline utilities for categorizing and formatting ObjectChange records.
"""

FIELD_DISPLAY_NAMES = {
    'name': 'Event ID',
    'summary': 'Summary',
    'status': 'Status',
    'start': 'Start Time',
    'end': 'End Time',
    'estimated_time_to_repair': 'Estimated Time to Repair',
    'acknowledged': 'Acknowledged',
    'internal_ticket': 'Internal Ticket',
    'comments': 'Comments',
    'original_timezone': 'Original Timezone',
    'provider': 'Provider',
    'impact': 'Impact Level',
}


def get_field_display_name(field_name):
    """
    Get human-readable display name for a field.

    Args:
        field_name: Database field name

    Returns:
        Human-readable field name
    """
    if field_name in FIELD_DISPLAY_NAMES:
        return FIELD_DISPLAY_NAMES[field_name]

    # Fallback: replace underscores and title case
    return field_name.replace('_', ' ').title()
