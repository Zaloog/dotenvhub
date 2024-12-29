import sys

from dotenvhub.tui import DotEnvHub
from dotenvhub.cli_parser import parse_args
from dotenvhub.constants import ENV_FILE_DIR_PATH, CONFIG_FILE_PATH
from dotenvhub.config import create_init_config
from dotenvhub.utils import (
    create_copy_in_cwd,
    get_env_content,
    create_shell_export_str,
    console,
)

__author__ = "Zaloog"
__copyright__ = "Zaloog"
__license__ = "MIT"


def main(args):
    create_init_config(conf_path=CONFIG_FILE_PATH, data_path=ENV_FILE_DIR_PATH)

    parsed_args = parse_args(args)

    if not args:
        DotEnvHub(config_path=CONFIG_FILE_PATH, data_path=ENV_FILE_DIR_PATH).run()

    if parsed_args.mode == "shell":
        content = get_env_content(filepath=ENV_FILE_DIR_PATH / parsed_args.filename)

        shell_str = create_shell_export_str(
            shell=parsed_args.shell, env_content=content
        )

        console.print(f"Copied [blue]{shell_str}[/] to clipboard")

    if parsed_args.mode == "copy":
        create_copy_in_cwd(
            filepath=ENV_FILE_DIR_PATH / parsed_args.filename,
            filename=parsed_args.export_name,
        )


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
