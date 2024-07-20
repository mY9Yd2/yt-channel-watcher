from datetime import UTC, datetime, timedelta, timezone
from typing import Any

from database.video_info import VideoInfo
from yt_dlp.postprocessor import PostProcessor
from yt_dlp.utils import DownloadCancelled


class VideoInfoPP(PostProcessor):
    def __init__(self, max_video_age_in_days: int):
        self.data: list[VideoInfo] = []
        super().__init__()
        self.__max_video_age_limit = datetime.now(timezone.utc) - timedelta(
            days=max_video_age_in_days
        )

    def run(self, info: dict[str, Any]):
        timestamp = datetime.fromtimestamp(info["timestamp"], UTC)

        if timestamp < self.__max_video_age_limit:
            raise DownloadCancelled(msg="The video is too old, stops")

        self.data.append(
            VideoInfo(
                uploader_id=info["uploader_id"],
                channel_id=info["channel_id"],
                channel=info["channel"],
                timestamp=timestamp,
                fulltitle=info["fulltitle"],
                display_id=info["display_id"],
                webpage_url=info["webpage_url"],
                thumbnail=info["thumbnail"],
                duration=info["duration"],
                duration_string=info["duration_string"],
            )
        )
        return [], info
