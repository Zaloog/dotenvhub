from pathlib import Path

from platformdirs import user_config_dir, user_data_dir

ENV_FILE_DIR = "env_files"

CONFIG_PATH = Path(
    user_config_dir(appname="dotenvhub", appauthor=False, ensure_exists=True)
)
DATA_PATH = Path(
    user_data_dir(appname="dotenvhub", appauthor=False, ensure_exists=True)
)
