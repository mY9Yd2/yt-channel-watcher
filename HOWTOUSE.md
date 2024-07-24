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

```text
pipx install --include-deps ./ytcw-0.1.0-py3-none-any.whl
```

## Configuration

```text
ytcw --help
```

## Run

Example:

```text
ytcw ytcw.sqlite3 channels.yaml dist/ --ydl-max-downloads=1
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
