from typing import Any

from ytcw.database.database import Database


def duplicate_check(info: dict[str, Any]) -> str | None:
    if "id" in info:
        video_info = Database().get_video_info_by_display_id(info["id"])
        if video_info is not None:
            return f"The {video_info.display_id} video is already exists in the database, ignore it"
