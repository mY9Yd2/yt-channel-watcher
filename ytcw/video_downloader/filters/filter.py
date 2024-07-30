"""
This module provides functionality for filtering video information
"""

from typing import Any

from ytcw.video_downloader.filters.duplicate_check import duplicate_check


def filter_video(info: dict[str, Any], *, incomplete: bool) -> str | None:
    """
    Filters the video information

    Filters:
        - Duplicate check: check if the video is already in the database

    Args:
        info (dict[str, Any]): A dictionary containing video information
        incomplete (bool): ???

    Returns:
        Returns a message indicating that the video should be ignored/filtered out
    """

    msg = duplicate_check(info)
    return msg
