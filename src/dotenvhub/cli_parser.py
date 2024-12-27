import argparse

from dotenvhub import __version__

from dotenvhub.config import DotEnvHubConfig
from dotenvhub.constants import SHELLS


def parse_args(args):
    cfg = DotEnvHubConfig()
    parser = argparse.ArgumentParser(description="DotEnvHub your .env file manager")
    subparsers = parser.add_subparsers(dest="mode")
    parser.add_argument(
        "--version",
        action="version",
        version=f"dotenvhub {__version__}",
    )
    sub_exp = subparsers.add_parser("copy", help="Export target File to CWD")
    sub_exp.add_argument(
        "filename",
        help="Export target File to CWD",
    )
    sub_exp.add_argument(
        "-N",
        "--name",
        help="Name of file to create in CWD",
        default=".env",
    )

    sub_copy = subparsers.add_parser(
        "shell", help="Shell to generate export string for"
    )
    sub_copy.add_argument(
        "filename",
        help="Filename where string is stored in DotEnvHub like FOLDER/FILE",
    )
    sub_copy.add_argument(
        "-S",
        "--shell",
        help=f"""
        Shell to generate Export String for
        (default: last selected shell in dotenvhub)
        (current:{cfg.shell})
        """,
        choices=SHELLS,
        default=cfg.shell,
    )

    return parser.parse_args(args)
