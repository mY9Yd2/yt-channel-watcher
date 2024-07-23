from typing import Any

from yt_dlp.utils import DownloadCancelled

from ytcw.database.database import Database


def duplicate_check(info: dict[str, Any]):
    if "id" in info:
        video_info = Database().get_video_info_by_display_id(info["id"])
        if video_info is not None:
            raise DownloadCancelled()
