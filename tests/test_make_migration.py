"""
Test to generate fresh migration for notices.
This is a utility test, not a real test.
"""

from io import StringIO

from django.core.management import call_command


def test_make_migration():
    """Generate migration for notices models"""
    out = StringIO()
    call_command("makemigrations", "notices", verbosity=2, stdout=out)
    output = out.getvalue()
    print(output)
    assert "Migrations for" in output or "No changes detected" in output
