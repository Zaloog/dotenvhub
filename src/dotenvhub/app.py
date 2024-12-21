import sys

from dotenvhub import cli_parser, constants, tui, utils

__author__ = "Zaloog"
__copyright__ = "Zaloog"
__license__ = "MIT"


def main(args):
    parsed_args = cli_parser.parse_args(args)

    if not args:
        tui.DotEnvHub().run()

    if parsed_args.mode == "shell":
        content = utils.get_env_content(
            filepath=constants.ENV_FILE_DIR_PATH / parsed_args.filename
        )

        shell_str = utils.create_shell_export_str(
            shell=parsed_args.shell, env_content=content
        )

        utils.console.print(f"Copied [blue]{shell_str}[/] to clipboard")

    if parsed_args.mode == "copy":
        utils.create_copy_in_cwd(
            filepath=constants.ENV_FILE_DIR_PATH / parsed_args.filename,
            filename=parsed_args.export_name,
        )


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
