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


def create_shell_export_str(shell, env_content):
    if shell == "pwsh":
        return create_pwsh_string(env_content=env_content)
    if shell == "cmd":
        return create_cmd_string(env_content=env_content)
    if shell == "bash":
        return create_bash_string(env_content=env_content)


def create_pwsh_string(env_content: str):
    lines = [var.split("=") for var in env_content.split("\n") if var]
    key_val_list = [f'$env:{key.strip()}="{val.strip()}"' for key, val in lines]
    pwsh_str = ";".join(key_val_list)
    pyperclip.copy(pwsh_str)
    return pwsh_str


def create_cmd_string(env_content: str):
    lines = [var.split("=") for var in env_content.split("\n") if var]
    key_val_list = [f'set "{key.strip()}={val.strip()}"' for key, val in lines]
    cmd_str = " & ".join(key_val_list)
    pyperclip.copy(cmd_str)
    return cmd_str


def create_bash_string(env_content: str):
    lines = [var.split("=") for var in env_content.split("\n") if var]
    key_val_list = [f"export {key.strip()}={val.strip()}" for key, val in lines]
    bash_str = " ; ".join(key_val_list)
    pyperclip.copy(bash_str)
    return bash_str
