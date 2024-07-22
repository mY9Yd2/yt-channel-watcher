from typing import Any

from database.database import Database
from yt_dlp.utils import DownloadCancelled


def duplicate_check(info: dict[str, Any]):
    if "id" in info:
        video_info = Database().get_video_info_by_display_id(info["id"])
        if video_info is not None:
            raise DownloadCancelled()
