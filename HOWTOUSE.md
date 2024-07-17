# How to use

## Table of contents

- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Channels](#channels)
- [Run](#run)

## Prerequisites

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) installed on the system
- templates/ folder

## Configuration

`config.json` example:

```json
{
    "maxDownloadsPerTab": 10,
    "maxVideoAgeInDays": 7
}
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

See my own list in the wiki.

## Run

```text
./yt-channel-watcher
```
