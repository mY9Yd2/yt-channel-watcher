from typing import Any

from rich.progress import (
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadCancelled, MaxDownloadsReached

from ytcw.database.database import Database
from ytcw.database.models import VideoInfo
from ytcw.filters.filter import filter_video
from ytcw.post_processors.video_info_pp import VideoInfoPP


class Downloader:
    def __init__(
        self,
        channels: dict[str, list[str]],
        ydl_max_downloads: int,
        ydl_max_video_age: int,
    ) -> None:
        self.__ydl_opts = {
            "extract_flat": "discard_in_playlist",
            "fragment_retries": 15,
            "extractor_retries": 15,
            "ignoreerrors": "only_download",
            "max_downloads": ydl_max_downloads,
            "noprogress": True,
            "postprocessors": [
                {"key": "FFmpegConcat", "only_multi_video": True, "when": "playlist"}
            ],
            "quiet": True,
            "retries": 15,
            "simulate": False,
            "skip_download": True,
            "match_filter": filter_video,
        }
        self.__ydl_extras = {"ydl_max_video_age": ydl_max_video_age}
        self.__channels = channels

    def __start(self, channel_name: str, path: str, print) -> list[VideoInfo]:
        print(f"\nDownloading [medium_purple3]{channel_name:<40} [orchid]/{path}")

        with YoutubeDL(self.__ydl_opts) as ydl:
            postprocessor = VideoInfoPP(self.__ydl_extras["ydl_max_video_age"])
            ydl.add_post_processor(postprocessor, "after_video")

            try:
                ydl.extract_info(f"https://www.youtube.com/{channel_name}/{path}")
            except (MaxDownloadsReached, DownloadCancelled) as err:
                print(err.msg)

            return postprocessor.data

    def start(self):
        progress_columns = [
            TextColumn("[progress.description]{task.description}"),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
            SpinnerColumn(),
        ]

        with Progress(*progress_columns) as progress:
            category_task = progress.add_task(
                "[cyan]Categories", total=len(self.__channels)
            )
            channels_task = progress.add_task(
                "[cyan]Channels",
                total=sum(len(value) for value in self.__channels.values()),
            )

            while not progress.finished:
                for category_name in self.__channels:
                    for channel_name in self.__channels[category_name]:
                        videos_data = self.__start(
                            channel_name, "videos", progress.console.print
                        )
                        if videos_data:
                            Database().insert_video_info_bulk(videos_data)

                        shorts_data = self.__start(
                            channel_name, "shorts", progress.console.print
                        )
                        if shorts_data:
                            Database().insert_video_info_bulk(shorts_data)

                        progress.update(channels_task, advance=1)
                    progress.update(category_task, advance=1)
            print()
