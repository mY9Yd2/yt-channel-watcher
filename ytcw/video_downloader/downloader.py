"""
This module defines the `Downloader` class, which uses `yt-dlp` to download video information from YouTube channels and stores it in a database
"""

from typing import Callable

from rich import print
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
from ytcw.video_downloader.filters.filter import filter_video
from ytcw.video_downloader.loggers.ydl_logger import YdlLogger
from ytcw.video_downloader.post_processors.video_info_pp import VideoInfoPP


class Downloader:
    """
    Downloader class to download video information from YouTube channels
    """

    def __init__(
        self,
        channels: dict[str, list[str]],
        ydl_max_downloads: int,
        ydl_max_video_age: int,
        skip_thumbnail_check: bool,
    ) -> None:
        """
        Initialises the Downloader with the specified parameters

        Args:
            channels (dict[str, list[str]]): Category dictionary and associated channel list
            ydl_max_downloads (int): Maximum number of downloads per tab/page/path
            ydl_max_video_age (int): Maximum age of the videos to be downloaded (exclusive)
            skip_thumbnail_check (bool): Whether to check for the existence of video thumbnails
        """

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
            "simulate": True,
            "match_filter": filter_video,
            "logger": YdlLogger(),
        }
        self.__ydl_extras = {"ydl_max_video_age": ydl_max_video_age}
        self.__channels = channels
        self.__skip_thumbnail_check = skip_thumbnail_check

    def __start(self, channel_name: str, path: str, print: Callable) -> list[VideoInfo]:
        """
        Downloads video information from a specified YouTube channel and path

        Args:
            channel_name (str): The name/id of the YouTube channel
            path (str): The path on the YouTube channel (e.g., 'videos', 'shorts')
            print (Callable): Function to print messages

        Returns:
            Returns a list of video information
        """

        print(f"\nDownloading [medium_purple3]{channel_name:<40} [orchid]/{path}")

        with YoutubeDL(self.__ydl_opts) as ydl:
            postprocessor = VideoInfoPP(
                self.__ydl_extras["ydl_max_video_age"], self.__skip_thumbnail_check
            )
            if channel_name.startswith("@"):
                postprocessor.uploader_id = channel_name

            ydl.add_post_processor(postprocessor, "video")

            try:
                ydl.extract_info(f"https://www.youtube.com/{channel_name}/{path}")
            except (MaxDownloadsReached, DownloadCancelled) as err:
                print(err.msg)

            return postprocessor.data

    def start(self) -> None:
        """
        Starts the download process for all channels specified during initialisation
        """

        progress_columns = [
            TextColumn("[progress.description]{task.description}"),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
            SpinnerColumn(),
        ]

        videos_count = 0
        shorts_count = 0

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
                            videos_count += len(videos_data)

                        shorts_data = self.__start(
                            channel_name, "shorts", progress.console.print
                        )
                        if shorts_data:
                            Database().insert_video_info_bulk(shorts_data)
                            shorts_count += len(shorts_data)

                        progress.update(channels_task, advance=1)
                    progress.update(category_task, advance=1)
            print()

        print(
            f"\nTotal number of new videos: {videos_count}\nTotal number of new shorts: {shorts_count}\n"
        )
