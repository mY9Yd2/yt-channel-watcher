# How to use

## Table of contents

- [Requirements](#requirements)
- [Install](#install)
- [Configuration](#configuration)
- [Run](#run)
- [Channels](#channels)

## Requirements

- [pipx](https://github.com/pypa/pipx) installed

## Install

See [pipx - Installing from Source Control](https://pipx.pypa.io/stable/#installing-from-source-control)

```text
pipx install --include-deps git+https://github.com/mY9Yd2/yt-channel-watcher.git
```

OR

```text
poetry build
```

```text
pipx install --include-deps ./dist/ytcw-0.1.0-py3-none-any.whl
```

## Configuration

```text
ytcw --help
```

## Run

Example:

```text
ytcw ytcw.sqlite3 channels.yaml --output dist/ --ydl-max-downloads=1
```

## Channels

`channels.json` example:

```json
{
    "vshojo": [
        "@IronMouseParty"
    ],
    "nijisanji": [
        "@MelocoKyoran",
        "@VictoriaBrightshield"
    ],
    "geexplus": [
        "@OniGiriEN"
    ],
    "independent": [
        "@Shylily"
    ]
}
```

OR

`channels.yaml` example:

```yml
---
vshojo:
- "@IronMouseParty"
nijisanji:
- "@MelocoKyoran"
- "@VictoriaBrightshield"
geexplus:
- "@OniGiriEN"
independent:
- "@Shylily"
```

See my own list in the wiki.
