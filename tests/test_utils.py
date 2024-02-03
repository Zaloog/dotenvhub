import sys
from pathlib import Path

import pytest

from dotenvhub import utils


@pytest.mark.skipif(sys.platform == "linux", reason="does not run on ubuntu")
def test_copy_path_to_clipboard():
    test_path = "test_folder/test_file"
    copied_path = utils.copy_path_to_clipboard(path=Path(test_path))
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
    copied_str = utils.create_shell_export_str(
        shell=shell, env_content=test_file_content
    )

    assert copied_str == expected_shell_str
