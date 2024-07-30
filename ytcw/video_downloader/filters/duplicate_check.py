"""
This module provides functionality for checking whether a video is a duplicate in the database
"""

from typing import Any

from ytcw.database.database import Database


def duplicate_check(info: dict[str, Any]) -> str | None:
    """
    Checks if the given video information corresponds to a video that already exists in the database.

    This function queries the database using the video's display id to check for duplicates.

    Args:
        info (dict[str, Any]): A dictionary containing video information

    Returns:
        Returns a message indicating that the video already exists in the database if a match is found; otherwise, None
    """

    if "id" in info:
        video_info = Database().get_video_info_by_display_id(info["id"])
        if video_info is not None:
            return f"The {video_info.display_id} video is already exists in the database, ignore it"
