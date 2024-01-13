import pyperclip


def copy_path_to_clipboard(path):
    pyperclip.copy(str(path))


def get_env_content(filepath):
    with open(filepath, "r") as env_file:
        return "".join(env_file.readlines())
