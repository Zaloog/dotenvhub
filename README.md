<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/dotenvhub.svg?branch=main)](https://cirrus-ci.com/github/<USER>/dotenvhub)
[![ReadTheDocs](https://readthedocs.org/projects/dotenvhub/badge/?version=latest)](https://dotenvhub.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/dotenvhub/main.svg)](https://coveralls.io/r/<USER>/dotenvhub)
[![PyPI-Server](https://img.shields.io/pypi/v/dotenvhub.svg)](https://pypi.org/project/dotenvhub/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/dotenvhub.svg)](https://anaconda.org/conda-forge/dotenvhub)
[![Monthly Downloads](https://pepy.tech/badge/dotenvhub/month)](https://pepy.tech/project/dotenvhub)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/dotenvhub)
-->

[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)

# dotenvhub

> Your Terminal App to manage your .env files

# Introduction
![header](https://raw.githubusercontent.com/Zaloog/dotenvhub/main/images/image_header.PNG)

DotEnvHub helps accessing your project specific .env files from a central place to setup your environment.

# Features
- Organizes files centrally under `user_data_dir` following the [XDG] Basedir Spec
- Saves your last selected shell automatically via a config file under `user_config_dir`
- Supports Creating/Editing/Deleting files in your dotenvhub
- Currently provides 3 ways to set your environment variables:
  1. Copy the shell specific command to set the environment variables into your clipboard
  2. Create a Copy of the selected file into your current working directory
  3. Copy the path of the selected file to be used with e.g. [python-dotenv] \
  without creating a copy in the project

# Installation
You can install dotenvhub with:
```bash
python -m pip install dotenvhub
```
Or using [pipx]
```bash
pipx install dotenvhub
```

# Usage
After Installation the Interface can be opened with:
```bash
dot
```

# Feedback and/or Issues
If you have feedback or find bugs, feel free to open an Issue


[XDG]: https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
[platformdirs]: https://platformdirs.readthedocs.io/en/latest/
[python-dotenv]: https://github.com/theskumar/python-dotenv
[pipx]: https://github.com/pypa/pipx
