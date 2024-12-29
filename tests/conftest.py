import pytest
from dotenvhub.tui import DotEnvHub
from dotenvhub.config import create_init_config
from dotenvhub.constants import ENV_FILE_DIR_NAME, CONFIG_FILE_NAME


@pytest.fixture
def test_conf_path(tmp_path) -> str:
    return tmp_path / CONFIG_FILE_NAME


@pytest.fixture
def test_data_path(tmp_path) -> str:
    (tmp_path / ENV_FILE_DIR_NAME).mkdir()
    return tmp_path / ENV_FILE_DIR_NAME


@pytest.fixture
def test_file_content() -> str:
    return """USER=TESTUSER
DB=TESTDB
PORT=TESTPORT
"""


@pytest.fixture
def test_dict() -> dict[str, str]:
    return {"USER": "TESTUSER", "DB": "TESTDB", "PORT": "TESTPORT"}


@pytest.fixture
def test_app(test_conf_path, test_data_path) -> DotEnvHub:
    create_init_config(conf_path=test_conf_path, data_path=test_data_path)
    return DotEnvHub(config_path=test_conf_path, data_path=test_data_path)
