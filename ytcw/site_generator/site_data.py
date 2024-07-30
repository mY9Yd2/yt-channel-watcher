"""
Module containing the SiteData dataclass, which holds the necessary information
to generate the website
"""

from dataclasses import dataclass, field
from typing import Any

from ytcw.database.models import VideoInfo


@dataclass
class SiteData:
    """
    Dataclass that encapsulates the data required for website generation

    Attributes:
        cfg (dict[str, Any]): The main application configuration settings
        channels (dict[str, list[str]]): Loaded channel identifiers and their associated categories
        video_infos (list[VideoInfo]): List of video information, including video title, channel name, etc.
        page (dict[str, Any]): Metadata and content information for the generated pages
    """

    cfg: dict[str, Any] = field(default_factory=dict)
    channels: dict[str, list[str]] = field(default_factory=dict)
    video_infos: list[VideoInfo] = field(default_factory=list)
    page: dict[str, Any] = field(default_factory=dict)
