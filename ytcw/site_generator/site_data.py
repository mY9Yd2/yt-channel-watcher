from dataclasses import dataclass, field
from typing import Any

from ytcw.database.video_info import VideoInfo


@dataclass
class SiteData:
    cfg: dict[str, Any] = field(default_factory=dict)
    channels: dict[str, list[str]] = field(default_factory=dict)
    video_infos: list[VideoInfo] = field(default_factory=list)
    page: dict[str, Any] = field(default_factory=dict)
