# Contributing

## Table of contents

- [Requirements](#requirements)
- [Install dependencies](#install-dependencies)
- [Run](#run)
- [Build and package](#build-and-package)
- [Code](#code)

## Requirements

- [poetry](https://python-poetry.org/) installed

- [isort](https://github.com/PyCQA/isort) / [isort - VSCode](https://marketplace.visualstudio.com/items?itemName=ms-python.isort)
- [black](https://github.com/psf/black)

or

- [ruff](https://github.com/astral-sh/ruff) / [ruff - VSCode](https://github.com/astral-sh/ruff-vscode)

Example VSCode config:

```json
"[python]": {
    "editor.formatOnType": true,
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.codeActionsOnSave": {
        "source.organizeImports": "explicit"
    }
}
```

## Install dependencies

```text
poetry install
```

## Run

```text
poetry run ytcw --help
```

## Build and package

```text
poetry build
```

## Code

Please sort the imports with `isort` and then use `black` for formating the source code
or just use `ruff` tool.
