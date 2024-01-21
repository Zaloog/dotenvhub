import argparse
import logging
import sys

from dotenvhub import __version__

from .constants import SHELLS


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="DotEnvHub your .env file manager")
    parser.add_argument(
        "--version",
        action="version",
        version=f"dotenvhub {__version__}",
    )
    parser.add_argument(
        "-s",
        "--scan",
        help="scan recursively for .env-files",
        action="store_true",
    )
    parser.add_argument(
        "-S",
        "--shell",
        dest="shell",
        choices=SHELLS,
        help="Select for which shell you want to generate export string",
    )
    parser.add_argument(
        "-E",
        "--export",
        dest="export",
        help="Export target File to CWD",
        action="store_true",
    )
    parser.add_argument(
        "-N",
        "--name",
        dest="filename",
        required=any(i in sys.argv for i in ["-S", "--shell"]),
        help="Which File to choose",
    )

    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)
