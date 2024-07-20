# How to use

## Table of contents

- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Channels](#channels)
- [Run](#run)

## Configuration

[Hydra doc](https://hydra.cc/docs/tutorials/basic/your_first_app/config_file/)

```text
poetry run python yt_channel_watcher/__main__.py --help
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

## Run

```text
poetry run python yt_channel_watcher/__main__.py
```
