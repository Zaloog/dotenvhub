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
    config["settings"] = {"Shell": "bash"}

    if not ENV_FILE_DIR_PATH.exists():
        data_path.mkdir(exist_ok=True)
        ENV_FILE_DIR_PATH.mkdir(exist_ok=True)

    with open(conf_path / CONFIG_FILE_NAME, "w") as configfile:
        config.write(configfile)


def check_config_exists(path=CONFIG_FILE_PATH):
    return path.exists()


class DotEnvHubConfig:
    def __init__(self, path=CONFIG_FILE_PATH) -> None:
        self.configpath = path
        self._config = configparser.ConfigParser(default_section=None)
        self._config.optionxform = str
        self._config.read(path)

    def save(self):
        with open(self.configpath, "w") as configfile:
            self.config.write(configfile)

    @property
    def config(self) -> configparser.ConfigParser:
        return self._config

    @property
    def shell(self) -> str:
        return self.config["settings"]["Shell"]

    @shell.setter
    def shell(self, new_shell) -> str:
        self._config["settings"]["Shell"] = new_shell
        self.save()


if not check_config_exists():
    create_init_config()

cfg = DotEnvHubConfig()
