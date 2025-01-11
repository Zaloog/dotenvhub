import os
from typing import Literal
import shutil
from pathlib import Path

import pyperclip
from rich.console import Console

from dotenvhub.constants import ENV_FILE_DIR_PATH

console = Console()


def update_file_tree(path: Path = ENV_FILE_DIR_PATH) -> dict:
    file_tree_dict = {}
    for dirpath, _, filenames in os.walk(path):
        rel_path = Path(dirpath).relative_to(path)
        file_tree_dict[f"{rel_path}"] = filenames

    return file_tree_dict


def copy_path_to_clipboard(path: Path) -> str:
    str_path = path.as_posix()
    pyperclip.copy(str_path)
    return str_path


def get_env_content(filepath: Path) -> str:
    try:
        with open(filepath, "r") as env_file:
            return env_file.read()
    except FileNotFoundError:
        console.print("File [red]not found[/], make sure you entered a valid filename")


def env_content_to_dict(content: str) -> dict[str, str]:
    content_dict = {}
    for line in content.splitlines():
        key, val = line.split("=")
        content_dict[key] = val

    return content_dict


def env_dict_to_content(content_dict: dict[str, str]) -> str:
    return "\n".join(["=".join([key, val]) for key, val in content_dict.items()])


def create_copy_in_cwd(filename: str, filepath: Path):
    try:
        shutil.copy(filepath, Path.cwd() / filename)
        console.print(f"Created [blue]{filename}[/] in CWD")
    except FileNotFoundError:
        console.print("File [red]not found[/], make sure you entered a valid filename")


def create_shell_export_str(
    shell: Literal["pwsh", "cmd", "bash", "zsh"], env_content: str
) -> str:
    if shell == "pwsh":
        return create_pwsh_string(env_content=env_content)
    if shell == "cmd":
        return create_cmd_string(env_content=env_content)
    if shell == "bash":
        return create_bash_string(env_content=env_content)
    if shell == "zsh":
        return create_bash_string(env_content=env_content)


def create_pwsh_string(env_content: str) -> str:
    lines = [var.split("=") for var in env_content.split("\n") if var]
    key_val_list = [f'$env:{key.strip()}="{val.strip()}"' for key, val in lines]
    pwsh_str = " ; ".join(key_val_list)
    pyperclip.copy(pwsh_str)
    return pwsh_str


def create_cmd_string(env_content: str) -> str:
    lines = [var.split("=") for var in env_content.split("\n") if var]
    key_val_list = [f'set "{key.strip()}={val.strip()}"' for key, val in lines]
    cmd_str = " & ".join(key_val_list)
    pyperclip.copy(cmd_str)
    return cmd_str


def create_bash_string(env_content: str) -> str:
    lines = [var.split("=") for var in env_content.split("\n") if var]
    key_val_list = [f"export {key.strip()}={val.strip()}" for key, val in lines]
    bash_str = " ; ".join(key_val_list)
    pyperclip.copy(bash_str)
    return bash_str


def write_to_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as env_file:
        env_file.write(content + "\n")
