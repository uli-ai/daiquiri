"""
Unit and regression test for the daiquiri package.
"""

# Import package, test suite, and other packages as needed
import daiquiri
import pytest
import sys

def test_daiquiri_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "daiquiri" in sys.modules
