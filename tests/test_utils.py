import pyperclip
import pytest

from dotenvhub import utils


def test_copy_path_to_clipboard():
    test_path = "test_folder/test_file"
    utils.copy_path_to_clipboard(path=test_path)
    assert test_path == pyperclip.paste()


@pytest.mark.parametrize(
    "shell, expected_shell_str ",
    [
        ("cmd", 'set "USER=TESTUSER" & set "DB=TESTDB" & set "PORT=TESTPORT"'),
        ("pwsh", '$env:USER="TESTUSER";$env:DB="TESTDB";$env:PORT="TESTPORT"'),
        ("bash", "export USER=TESTUSER ; export DB=TESTDB ; export PORT=TESTPORT"),
        ("zsh", "export USER=TESTUSER ; export DB=TESTDB ; export PORT=TESTPORT"),
    ],
)
def test_create_shell_export_str(shell, test_file_content, expected_shell_str):
    utils.create_shell_export_str(shell=shell, env_content=test_file_content)
    test_str = pyperclip.paste()

    assert test_str == expected_shell_str
