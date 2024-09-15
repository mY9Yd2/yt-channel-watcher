"""
This module defines a custom post-processor that collects video information
"""

from datetime import UTC, datetime, timedelta
from typing import Any

import requests
from yt_dlp.postprocessor import PostProcessor
from yt_dlp.utils import DownloadCancelled

from ytcw.database.models import VideoInfo


class VideoInfoPP(PostProcessor):
    """
    A post-processor to collect video information and optionally check for available thumbnails

    Attributes:
        data (list[VideoInfo]): A list to store collected video information
    """

    def __init__(self, ydl_max_video_age: int, skip_thumbnail_check: bool):
        """
        Initialising the post-processor

        Args:
            ydl_max_video_age (int): The maximum age limit, in days for videos to be processed
            check_thumbnail (bool): Flag to indicate whether thumbnails should be checked for availability
        """

        self.data: list[VideoInfo] = []
        super().__init__()
        self.__max_video_age_limit = datetime.now(UTC) - timedelta(
            days=ydl_max_video_age
        )
        self.__skip_thumbnail_check = skip_thumbnail_check
        self.uploader_id = None

    def run(self, info: dict[str, Any]):
        """
        Processes the video information and updates the internal list of video data

        Args:
            info (dict[str, Any]): A dictionary containing video information

        Returns:
            This method returns a tuple, the first element is a list of the files
            that can be deleted, and the second of which is the updated information

        Raises:
            DownloadCancelled: If the video is older than the maximum allowed age
        """

        timestamp = datetime.fromtimestamp(info["timestamp"], UTC)

        if timestamp < self.__max_video_age_limit:
            raise DownloadCancelled(msg="The video is too old, stops")

        selected_thumbnail = (
            self.__get_thumbnail(
                display_id=info["display_id"],
                thumbnails=info.get("thumbnails", []),
            )
            or info["thumbnail"]
        )

        if info["uploader_id"] is None:
            info["uploader_id"] = self.uploader_id

        self.data.append(
            VideoInfo(
                uploader_id=info["uploader_id"],
                channel_id=info["channel_id"],
                channel=info["channel"],
                timestamp=timestamp,
                fulltitle=info["fulltitle"],
                display_id=info["display_id"],
                webpage_url=info["webpage_url"],
                thumbnail=selected_thumbnail,
                duration=info["duration"],
                duration_string=info["duration_string"],
                language=info.get("language"),
            )
        )
        return [], info

    def __get_thumbnail(self, display_id: str, thumbnails: list[dict[str, str | int]]):
        """
        Determines the appropriate thumbnail URL based on the provided information and the configuration

        Args:
            display_id (str): The display id of the video.
            thumbnails (list[dict[str, str | int]]): A list of thumbnail information dictionaries

        Returns:
            Returns the URL of the selected thumbnail or None if no suitable thumbnail is found
        """

        if self.__skip_thumbnail_check:
            return self.__find_thumbnail_from_list(thumbnails)
        else:
            return self.__find_available_thumbnail(display_id)

    def __find_available_thumbnail(self, display_id: str) -> str | None:
        """
        Attempts to find an available thumbnail by checking a list of known thumbnail names

        Args:
            display_id (str): The display id of the video

        Returns:
            Returns the URL of the available thumbnail or None if no available thumbnail is found
        """

        thumbnails_names = ["sddefault.webp", "hqdefault.webp", "0.webp"]
        base_url = f"https://i.ytimg.com/vi_webp/{display_id}/"
        for file_name in thumbnails_names:
            url = f"{base_url}{file_name}"
            try:
                res = requests.head(url, timeout=5)
                if res.status_code == 200:
                    return url
            except (requests.ConnectionError, requests.Timeout):
                continue

    def __find_thumbnail_from_list(
        self, thumbnails: list[dict[str, str | int]]
    ) -> str | None:
        """
        Finds a thumbnail URL from a list of provided thumbnails

        Args:
            thumbnails (list[dict[str, str | int]]): A list of thumbnail information dictionaries

        Returns:
            Returns the URL of the thumbnail that ends with a given name, or None if not found
        """

        for thumbnail in thumbnails:
            url = thumbnail.get("url", "")
            if url.endswith("sddefault.webp"):
                return url
