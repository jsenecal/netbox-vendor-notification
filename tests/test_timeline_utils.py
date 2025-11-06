import pytest
from vendor_notification.timeline_utils import get_field_display_name


class TestFieldDisplayNames:
    def test_get_field_display_name_maps_known_fields(self):
        assert get_field_display_name("name") == "Event ID"
        assert get_field_display_name("status") == "Status"
        assert get_field_display_name("start") == "Start Time"
        assert get_field_display_name("acknowledged") == "Acknowledged"

    def test_get_field_display_name_handles_unknown_fields(self):
        # Should return titlecased field name with underscores replaced
        assert get_field_display_name("unknown_field") == "Unknown Field"
        assert get_field_display_name("custom") == "Custom"
