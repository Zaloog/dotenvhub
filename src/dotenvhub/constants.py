from pathlib import Path

from platformdirs import user_config_dir, user_data_dir

ENV_FILE_DIR_NAME = "env_files"
CONFIG_FILE_NAME = "dotenvhub.ini"

CONFIG_PATH = Path(
    user_config_dir(appname="dotenvhub", appauthor=False, ensure_exists=True)
)
DATA_PATH = Path(
    user_data_dir(appname="dotenvhub", appauthor=False, ensure_exists=True)
)

CONFIG_FILE_PATH = CONFIG_PATH / CONFIG_FILE_NAME
ENV_FILE_DIR_PATH = DATA_PATH / ENV_FILE_DIR_NAME

SHELLS = [
    "pwsh",
    "cmd",
    "bash",
    "zsh",
]
