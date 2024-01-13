import configparser

from .constants import (
    CONFIG_FILE_NAME,
    CONFIG_FILE_PATH,
    CONFIG_PATH,
    DATA_PATH,
    ENV_FILE_DIR_PATH,
)


def create_init_config(conf_path=CONFIG_PATH, data_path=DATA_PATH):
    config = configparser.ConfigParser(default_section=None)
    config.optionxform = str
    config["settings"] = {"Used_Shell": "pwsh"}

    if not ENV_FILE_DIR_PATH.exists():
        data_path.mkdir(exist_ok=True)
        ENV_FILE_DIR_PATH.mkdir(exist_ok=True)

    with open(conf_path / CONFIG_FILE_NAME, "w") as configfile:
        config.write(configfile)


def check_config_exists(path=CONFIG_FILE_PATH):
    return path.exists()
