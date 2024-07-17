# yt-channel-watcher

## Table of contents

- [About](#about)
- [Short story, background](#short-story-background)
- [How to use](#how-to-use)
- [Errors](#errors)
- [Contributing](#contributing)
- [License](#license)

![Screenshot of the html output](screenshot.png)

## About

yt-channel-watcher is a program that call [yt-dlp](https://github.com/yt-dlp/yt-dlp) to fetch channels informations (videos&shorts) and then generate a static HTML from the video data.  
I really liked the [holodex](https://holodex.net/) project, but it only tracks vtuber clippers and I really wanted to see only the vtubers' own creations.  
This project is not limited to just to the vtuber community, you can use it to fetch any youtube channel.

### Short story, background

This project was originally written in JavaScript and wrote the returned json to the file system. (~700 MB, with lots of channels and unused json data).  
On a whim I installed a NetBSD on my RPI0 (1 core) and was unable to install a binary version of NodeJS on it. So I needed a quick and easy solution to cross compile and deploy. So I decided to use Go, even though I had never touched it before.  
While I'm at it, let's improve the code too! Spending 2+ hours just to fetch&build the html just seems wrong.

## How to use

[See HOWTOUSE.md](HOWTOUSE.md)

## Errors

There are some error logs that can be confusing. You can ignore them.

```text
2024/07/15 10:06:46 stderr:
2024/07/15 10:06:46 stderr: ERROR: Interrupted by user
2024/07/15 10:06:46 Command exited with status code: 1
```

```text
2024/07/15 10:05:58 stderr: ERROR: [youtube:tab] @KanadeIzuru: This channel does not have a shorts tab
2024/07/15 10:05:58 Command exited with status code: 1
```

```text
2024/07/15 10:44:15 stderr: ERROR: [youtube:tab] @AkaiHaato_Sub: This channel does not have a videos tab
2024/07/15 10:44:15 Command exited with status code: 1
```

```text
2024/07/15 09:58:59 stderr: ERROR: [youtube] EVKGLK4NPXU: Premieres in 6 hours
```

## Contributing

[See CONTRIBUTING.md](CONTRIBUTING.md)

## License

The project is licensed under the MIT licence.
