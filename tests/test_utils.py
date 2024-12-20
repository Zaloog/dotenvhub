import sys
from pathlib import Path

import pytest

from dotenvhub.utils import (
    copy_path_to_clipboard,
    create_shell_export_str,
    env_content_to_dict,
    env_dict_to_content,
)


@pytest.mark.skipif(sys.platform == "linux", reason="does not run on ubuntu")
def test_copy_path_to_clipboard():
    test_path = "test_folder/test_file"
    copied_path = copy_path_to_clipboard(path=Path(test_path))
    assert test_path == copied_path


@pytest.mark.skipif(sys.platform == "linux", reason="does not run on ubuntu")
@pytest.mark.parametrize(
    "shell, expected_shell_str ",
    [
        ("cmd", 'set "USER=TESTUSER" & set "DB=TESTDB" & set "PORT=TESTPORT"'),
        ("pwsh", '$env:USER="TESTUSER" ; $env:DB="TESTDB" ; $env:PORT="TESTPORT"'),
        ("bash", "export USER=TESTUSER ; export DB=TESTDB ; export PORT=TESTPORT"),
        ("zsh", "export USER=TESTUSER ; export DB=TESTDB ; export PORT=TESTPORT"),
    ],
)
def test_create_shell_export_str(shell, test_file_content, expected_shell_str):
    copied_str = create_shell_export_str(shell=shell, env_content=test_file_content)
    assert copied_str == expected_shell_str


def test_env_content_to_dict(test_file_content):
    result = env_content_to_dict(content=test_file_content)
    assert result == {"USER": "TESTUSER", "DB": "TESTDB", "PORT": "TESTPORT"}


def test_env_dict_to_content(test_dict):
    result = env_dict_to_content(content_dict=test_dict)
    assert result == """USER=TESTUSER\nDB=TESTDB\nPORT=TESTPORT"""
