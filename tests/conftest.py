"""
    Dummy conftest.py for dotenvhub.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pytest


@pytest.fixture
def test_file_content():
    return """
USER=TESTUSER
DB=TESTDB
PORT=TESTPORT
"""
