"""
Pytest configuration for notices tests.
Sets up Django and NetBox environment for testing.
"""

import os
import sys

# Add NetBox to Python path BEFORE any imports
sys.path.insert(0, "/opt/netbox/netbox")

# Configure NetBox to use testing configuration
os.environ["NETBOX_CONFIGURATION"] = "netbox.configuration_testing"

# Set Django settings module to netbox.settings (NOT configuration_testing)
os.environ["DJANGO_SETTINGS_MODULE"] = "netbox.settings"

# Import and configure testing settings BEFORE pytest starts
from netbox import configuration_testing

# Configure database for testing
# Use PostgreSQL (required for NetBox - SQLite doesn't support array fields)
configuration_testing.DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "netbox"),
        "USER": os.environ.get("DB_USER", "netbox"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "postgres"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "CONN_MAX_AGE": 300,
    }
}

# Add notices to PLUGINS
if not hasattr(configuration_testing, "PLUGINS"):
    configuration_testing.PLUGINS = []
if "notices" not in configuration_testing.PLUGINS:
    configuration_testing.PLUGINS.append("notices")

# Set default PLUGINS_CONFIG if not present
if not hasattr(configuration_testing, "PLUGINS_CONFIG"):
    configuration_testing.PLUGINS_CONFIG = {}

if "notices" not in configuration_testing.PLUGINS_CONFIG:
    configuration_testing.PLUGINS_CONFIG["notices"] = {}

# Initialize Django BEFORE test collection
import django

django.setup()


def pytest_configure(config):
    """
    Hook called after command line options have been parsed.
    Django is already set up at module import time above.
    """
    pass
