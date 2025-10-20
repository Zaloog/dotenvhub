[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI-Server](https://img.shields.io/pypi/v/dotenvhub.svg)](https://pypi.org/project/dotenvhub/)
[![Pyversions](https://img.shields.io/pypi/pyversions/dotenvhub.svg)](https://pypi.python.org/pypi/dotenvhub)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/dotenvhub)](https://pepy.tech/project/dotenvhub)

# dotenvhub

> Your Terminal App to manage your .env files

# Introduction
![header](https://raw.githubusercontent.com/Zaloog/dotenvhub/main/images/demo.gif)

DotEnvHub helps storing and accessing your project specific .env files from a central place to setup your environment variables.
Supporting you to follow the [12-factor] principles when developing applications.

# Features
- Organizes files centrally under `user_data_dir` following the [XDG] Basedir Spec
- Saves your last selected shell automatically via a config file under `user_config_dir`
- Supports Creating/Editing/Deleting files in your dotenvhub
- Simple Navigation using [textual-jumper] to display a jump overlay
- Currently provides 3 ways to set your environment variables:
  1. Copy the Shell specific command to set the environment variables into your clipboard
  2. Create a Copy of the selected file into your current working directory
  3. Copy the path of the selected file to be used with e.g. [python-dotenv] \
  without creating a copy in the project

# Installation
You can install `dotenvhub` with one of the following options:

```bash
# not recommended
python -m pip install dotenvhub
```
```bash
pipx install dotenvhub
```

```bash
uv tool install dotenvhub
```
I recommend using [pipx] or [uv] to install CLI Tools into an isolated environment.

# Usage
## Using the Graphical UI

After Installation the Interface can be opened with:
```bash
dot
```
Use `Ctrl+q` to close the interface.

## Using the CLI
The Creation of a Copy in the CWD and copying the Shell String
to set the environment variables can also be done directly in the CLI:

To create a copy of `FOLDER/FILE` from DotEnvHub and save it as `SAVENAME` in your CWD:
```bash
dot copy <FOLDER/FILE> -N <SAVENAME>
```

To copy the string to clipboard to set `FOLDER/FILE` from DotEnvHub in your `Shell` of Choice:
```bash
dot shell <FOLDER/FILE> -S <SHELL>
```

# Feedback and/or Issues
If you have feedback or find bugs, feel free to open an Issue.

:warning: DotEnvHub uses `pyperclip` to handle copy/paste actions.
Based on the pyperclips documentation, you might need additional packages installed
on linux systems like `xclip` or `xsel` which can be installed with:

```bash
sudo apt-get install xclip
sudo apt-get install xsel
```

like mentioned [here](https://pyperclip.readthedocs.io/en/latest/)


[XDG]: https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
[platformdirs]: https://platformdirs.readthedocs.io/en/latest/
[python-dotenv]: https://github.com/theskumar/python-dotenv
[pipx]: https://github.com/pypa/pipx
[12-factor]: https://12factor.net
[uv]: https://docs.astral.sh/uv
[textual-jumper]: https://github.com/Zaloog/textual-jumper
