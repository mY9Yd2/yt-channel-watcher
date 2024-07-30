from datetime import UTC, datetime, timedelta
from typing import Any

import requests
from yt_dlp.postprocessor import PostProcessor
from yt_dlp.utils import DownloadCancelled

from ytcw.database.models import VideoInfo


class VideoInfoPP(PostProcessor):
    def __init__(self, ydl_max_video_age: int, check_thumbnail: bool):
        self.data: list[VideoInfo] = []
        super().__init__()
        self.__max_video_age_limit = datetime.now(UTC) - timedelta(
            days=ydl_max_video_age
        )
        self.__check_thumbnail = check_thumbnail

    def run(self, info: dict[str, Any]):
        timestamp = datetime.fromtimestamp(info["timestamp"], UTC)

        if timestamp < self.__max_video_age_limit:
            raise DownloadCancelled(msg="The video is too old, stops")

        selected_thumbnail = (
            self._get_thumbnail(
                display_id=info["display_id"],
                thumbnails=info.get("thumbnails", []),
            )
            or info["thumbnail"]
        )

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

    def _get_thumbnail(self, display_id: str, thumbnails: list[dict[str, str | int]]):
        if self.__check_thumbnail:
            return self._find_available_thumbnail(display_id)
        else:
            return self._find_thumbnail_from_list(thumbnails)

    def _find_available_thumbnail(self, display_id: str) -> str | None:
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

    def _find_thumbnail_from_list(
        self, thumbnails: list[dict[str, str | int]]
    ) -> str | None:
        for thumbnail in thumbnails:
            url = thumbnail.get("url", "")
            if url.endswith("sddefault.webp"):
                return url
