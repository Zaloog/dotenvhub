"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = dotenvhub.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import sys

from dotenvhub import cli_parser, constants, tui, utils

__author__ = "Zaloog"
__copyright__ = "Zaloog"
__license__ = "MIT"


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from dotenvhub.skeleton import fib`,
# when using this Python module as a library.


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
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
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m dotenvhub.skeleton 42
    #
    run()
