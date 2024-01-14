import shutil
from pathlib import Path

import pyperclip


def copy_path_to_clipboard(path):
    pyperclip.copy(str(path))


def get_env_content(filepath: Path):
    with open(filepath, "r") as env_file:
        return "".join(env_file.readlines())


def create_copy_in_cwd(filename: str, filepath: Path):
    cwd = Path.cwd()
    shutil.copy(filepath, cwd / filename)
