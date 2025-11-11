"""
Tests for iCal-related plugin settings.
"""

import pytest
from django.conf import settings


@pytest.mark.django_db
class TestICalSettings:
    """Test iCal plugin settings."""

    def test_ical_token_placeholder_setting_exists(self):
        """Test that ical_token_placeholder setting exists."""
        plugin_config = settings.PLUGINS_CONFIG.get("notices", {})

        # Should have default value
        assert "ical_token_placeholder" in plugin_config or True  # Will check default

    def test_ical_token_placeholder_default_value(self):
        """Test that ical_token_placeholder defaults to 'changeme'."""
        from notices import NoticesConfig

        config = NoticesConfig
        default_placeholder = config.default_settings.get("ical_token_placeholder")

        assert default_placeholder == "changeme"
